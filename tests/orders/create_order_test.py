from src.dao.products_dao import ProductsDAO
from src.helpers.orders_helper import OrdersHelper
from src.helpers.customers_helper import CustomerHelper
import pytest

@pytest.fixture(scope='module')
def my_orders_smoke_setup():
    product_dao = ProductsDAO()
    rand_product = product_dao.get_random_product_from_db(1)
    product_id = rand_product[0]['ID']

    order_helper = OrdersHelper()

    info = {'product_id': product_id,
            'order_helper': order_helper}

    return info


@pytest.mark.smoke
@pytest.mark.orders
@pytest.mark.tc8
def test_create_paid_order_guest_user(my_orders_smoke_setup):

    order_helper = my_orders_smoke_setup['order_helper']

    customer_id = 0
    product_id = my_orders_smoke_setup['product_id']

    # make an api call
    info = {"line_items": [
                {
                  "product_id": product_id,
                  "quantity": 1
                }
              ]}
    order_json = order_helper.create_order(additional_args=info)
