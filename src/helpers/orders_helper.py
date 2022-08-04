from src.utilities.wooAPIUtility import WooAPIUtility
from src.utilities.requestsUtility import RequestsUtility
from src.dao.orders_dao import OrdersDAO
import os
import json

class OrdersHelper(object):

    def __init__(self):
        self.cur_file_dir = os.path.dirname(os.path.realpath(__file__))
        self.woo_helper = WooAPIUtility()
        self.request_helper = RequestsUtility()

    def create_order(self, additional_args=None):

        # setting body for the api request
        body_template = os.path.join(self.cur_file_dir, '..', 'data', 'create_order_payload.json')

        # open that file and modify it from json to python
        with open(body_template) as f:
            request_body = json.load(f)

        # if user adds more info to payload, then update it
        if additional_args:
            assert isinstance(additional_args, dict), f"Parameter 'additional_args' must be a dictionary but found {type(additional_args)}"
            request_body.update(additional_args)

        api_response = self.request_helper.post('orders', body_params=request_body, expected_status_code=201)

        return api_response

    @staticmethod  # Main purpose is to contain logic pertaining to the class, but that logic should not have any need for specific class instance data.
    def verify_order_is_created(order_json, exp_cust_id, exp_products):
        orders_dao = OrdersDAO()

        # verify response
        assert order_json, f"Create order response is empty."
        assert order_json['customer_id'] == exp_cust_id, f"Create order with given customer id returned " \
                                                         f"bad customer id. Expected customer_id={exp_cust_id} but got " \
                                                         f"'{order_json['customer_id']}'"

        assert len(order_json['line_items']) == len(exp_products), f"Expected only {len(exp_products)} item in order but " \
                                                                   f"found '{len(order_json['line_items'])}'" \
                                                                   f"Order id: {order_json['id']}."

        # verify db
        order_id = order_json['id']
        line_info = orders_dao.get_order_lines_by_order_id(order_id)
        assert line_info, f"Create order, line item not found in DB. Order id: {order_id}"

        # loop through db table to fetch one order item with 'order_item_type' key that equals 'line_item' value
        line_items = [i for i in line_info if i['order_item_type'] == 'line_item']
        assert len(line_items) == 1, f"Expected 1 line item but found {len(line_items)}. Order id: {order_id}"

        # get one item from the db
        line_item_id = line_items[0]['order_item_id']
        line_details = orders_dao.get_order_items_details(line_item_id)

        # verify db product id matches api product id
        db_product_id = int(line_details['_product_id'])
        api_product_id = order_json['line_items'][0]['product_id']
        assert db_product_id == api_product_id, \
            f"Create order product id in db {db_product_id} does not match product id in api response {api_product_id}"

        # get list of product ids in the response
        api_product_ids = [i['product_id'] for i in order_json['line_items']]
        for product in exp_products:
            assert product['product_id'] in api_product_ids, f"Create order does not have at least 1 expected product in DB." \
                                                             f"Product id: {product['product_id']}. Order id: {order_id}"

    def call_update_an_order(self, order_id, payload):
        return self.request_helper.put(f'orders/{order_id}', body_params=payload)

    def call_get_an_order(self, order_id):
        return self.request_helper.get(f"orders/{order_id}")
