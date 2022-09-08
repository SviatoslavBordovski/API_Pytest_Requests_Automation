from src.helpers.orders_helper import OrdersHelper
from src.utilities.wooAPIUtility import WooAPIUtility
from src.utilities.genericUtilities import generate_random_string
import pytest

pytestmark = [pytest.mark.orders, pytest.mark.regression]

@pytest.mark.parametrize("new_status",
                         [
                             pytest.param('cancelled', marks=pytest.mark.tc10),
                             pytest.param('completed', marks=pytest.mark.tc11),
                             pytest.param('on-hold', marks=pytest.mark.tc12),
                         ])
def test_update_order_status(new_status):

    # create a new order
    order_helper = OrdersHelper()
    order_json = order_helper.create_order()
    cur_status = order_json['status']
    assert cur_status != new_status, f"Current status of order is already {new_status}. " \
                                     f"Unable to run test."

    # update the status with the body params
    order_id = order_json['id']
    payload = {"status": new_status}
    order_helper.call_update_an_order(order_id, payload)

    # get order information
    new_order_info = order_helper.call_get_an_order(order_id)

    # verify new actual order status equals expected updated status
    assert new_order_info['status'] == new_status, f"Updated order status to '{new_status}', " \
                                                   f"but order is still '{new_order_info['status']}'"


@pytest.mark.tc13
def test_update_order_status_to_random_string():

    new_status = 'abcdefg'

    # create new order
    order_helper = OrdersHelper()
    order_json = order_helper.create_order()
    order_id = order_json['id']

    # update the status
    payload = {"status": new_status}
    rs_api = WooAPIUtility().put(f'orders/{order_id}', params=payload, expected_status_code=400)

    assert rs_api['code'] == 'rest_invalid_param', f"Update order status to random string did not have " \
         f"correct code in response. Expected: 'rest_invalid_param' Actual: {rs_api['code']}"

    assert rs_api['message'] == 'Invalid parameter(s): status',  f"Update order status to random " \
     f"string did not have correct messge in response. " \
     f"Expected: 'rest_invalid_param' Actual: {rs_api['message']}"

@pytest.mark.tc14
def test_update_order_customer_note():

    order_helper = OrdersHelper()
    order_json = order_helper.create_order()
    order_id = order_json['id']

    rand_string = generate_random_string(40)
    payload = {"customer_note": rand_string}
    order_helper.call_update_an_order(order_id, payload)

    # get order information
    new_order_info = order_helper.call_get_an_order(order_id)
    assert new_order_info['customer_note'] == rand_string, f"Update order's 'customer_note' field," \
       f"failed. Expected: {rand_string}, Actual: {new_order_info['customer_note']}"
