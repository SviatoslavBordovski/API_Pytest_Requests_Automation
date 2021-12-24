from src.utilities.requestsUtility import RequestsUtility
from src.dao.products_dao import ProductsDAO
from src.helpers.products_helper import ProductsHelper
import pytest

@pytest.mark.products
@pytest.mark.tc4
def test_get_all_products():
    request_sent = RequestsUtility()
    api_response = request_sent.get(endpoint='products')
    assert api_response, f"Response of all products list is empty"

@pytest.mark.products
@pytest.mark.tc5
def test_get_product_by_id():

    # get a product data (id, name and status) from db
    rand_product = ProductsDAO().get_random_product_from_db(1)
    rand_product_id = rand_product[0]['ID']
    product_db_name = rand_product[0]['post_title']
    product_status = rand_product[0]['post_status']

    # make the 'get' api request
    product_helper = ProductsHelper()
    rs_api = product_helper.get_product_by_id(rand_product_id)
    api_name = rs_api['name']
    api_post_status = rs_api['status']

    # verify the response for name and product status
    assert product_db_name == api_name, f"Get product by id returned wrong product. Product id: {rand_product_id}, " \
                                f"Db name: {product_db_name}, Api name: {api_name}"

    assert product_status == api_post_status, f"Returned product has wrong status. Product id: {rand_product_id}" \
                                f"Db status: {product_status}, Api status: {api_post_status}"
