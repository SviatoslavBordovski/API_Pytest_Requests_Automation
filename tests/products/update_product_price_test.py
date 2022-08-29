from src.helpers.products_helper import ProductsHelper
from src.dao.products_dao import ProductsDAO
from src.utilities.genericUtilities import generate_random_string, generate_random_integer
import random
import pytest

pytestmark = [pytest.mark.products, pytest.mark.regression]

@pytest.mark.tc15
def test_update_regular_price_should_updated_price():
    """In this test 'sale_price' of the product must be empty. If product has sale price, updating the 'regular_price'
    does not update the 'price'. So get a bunch of products and loop until you find one that is not on sale. If all in
    the list are on sale then take random one and update the sale price"""

    product_helper = ProductsHelper()

    # get random product from the db and prepare needed data
    products_basket = ProductsDAO().get_random_product_from_db(30)
    random_price_number = generate_random_integer()
    payload = {'regular_price': random_price_number}

    for product in products_basket:
        product_id = product['ID']
        product_data = product_helper.call_retrieve_product(product_id)
        if product_data['on_sale']:
            continue
        else:
            break

    else:
        # take a random product and make it not on sale by setting {'sale_price': ''}
        test_product = random.choice(products_basket)
        product_id = test_product['ID']
        product_helper.call_update_product(product_id, {'sale_price': ''})

    # api call to update product and then get that product by id
    product_helper.call_update_product(product_id, payload)
    updated_rs_api = product_helper.call_retrieve_product(product_id)

    assert updated_rs_api['regular_price'] == random_price_number, f"Payload is {payload}, 'regular_price' api " \
                                                                   f"response => {updated_rs_api['regular_price']}, " \
                                                                   f"'price' api response => {updated_rs_api['price']}"

    assert updated_rs_api['price'] == random_price_number, f"Payload is {payload}, 'regular_price' api response => " \
                                                           f"{updated_rs_api['regular_price']}, 'price' api " \
                                                           f"response => {updated_rs_api['price']}"
