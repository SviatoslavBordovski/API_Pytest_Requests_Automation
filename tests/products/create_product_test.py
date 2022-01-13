from src.utilities.genericUtilities import generate_random_string
from src.helpers.products_helper import ProductsHelper
from src.dao.products_dao import ProductsDAO
import pytest

@pytest.mark.products
@pytest.mark.tc6
def test_create_1_simple_product():

    # generate dictionary and data for it
    request_body = dict()
    request_body['name'] = generate_random_string(10, prefix="automation_test_name_")
    request_body['type'] = "simple"
    request_body['regular_price'] = "10.99"
    request_body['description'] = generate_random_string(30, suffix="_quite_good_described_field")

    # make the api call
    product_rs = ProductsHelper().call_create_product(request_body)

    # verify the response is not empty and actual result matches expected
    assert product_rs, f"Create product api response is empty. Request body is: {request_body}"
    assert product_rs['name'] == request_body['name'], f"Create product api call response has" \
        f"unexpected name. Expected: {request_body['name']}, Actual: {product_rs['name']}"

    # verify the product exists in db
    product_id = product_rs['id']
    db_product = ProductsDAO().get_product_by_id(product_id)

    # verify api product name matches recorded db product name
    assert request_body['name'] == db_product[0]['post_title'], f"Create product, title in db does not match " \
        f"title in api. DB: {db_product['post_title']}, API: {request_body['name']}"
