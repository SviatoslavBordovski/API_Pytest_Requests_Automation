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
