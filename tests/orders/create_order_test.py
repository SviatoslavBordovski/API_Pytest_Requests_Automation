from src.dao.products_dao import ProductsDAO
from src.helpers.orders_helper import OrdersHelper
from src.helpers.customers_helper import CustomerHelper
import logging as logger
import pytest

@pytest.fixture(scope='module')
def orders_setup():
    product_dao = ProductsDAO()
    order_helper = OrdersHelper()
    
    rand_product = product_dao.get_random_product_from_db(1)
    product_id = rand_product[0]['ID']

    info = {'product_id': product_id,
            'order_helper': order_helper}

    return info


@pytest.mark.orders
@pytest.mark.tc8
def test_create_order_guest_user(orders_setup):

    logger.info("Test Case #8: Create a new paid order by guest user.")

    order_helper = orders_setup['order_helper']

    customer_id = 0
    product_id = orders_setup['product_id']

    # make an api call
    info = {"line_items": [
                {
                  "product_id": product_id,
                  "quantity": 1
                }
              ]}
    order_json = order_helper.create_order(additional_args=info)

    # verify response
    expected_product = [{'product_id': product_id}]
    order_helper.verify_order_is_created(order_json, customer_id, expected_product)

@pytest.mark.orders
@pytest.mark.tc9
def test_create_paid_order_new_created_customer(my_orders_smoke_setup):
    
    # create helper objects
    order_helper = my_orders_smoke_setup['order_helper']
    customer_helper = CustomerHelper()

    # make the call
    cust_info = customer_helper.create_customer()
    customer_id = cust_info['id']
    product_id = my_orders_smoke_setup['product_id']

    info = {"line_items": [
                {
                  "product_id": product_id,
                  "quantity": 1
                }
              ],
    "customer_id": customer_id
    }

    order_json = order_helper.create_order(additional_args=info)

    # verify response
    expected_products = [{'product_id': product_id}]
    order_helper.verify_order_is_created(order_json, customer_id, expected_products)
