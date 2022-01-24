from src.helpers.products_helper import ProductsHelper
from src.dao.products_dao import ProductsDAO
import logging as logger
import pytest
from datetime import datetime, timedelta

@pytest.mark.regression
class TestListProductsWithFilter(object):

    @pytest.mark.tc7
    def test_list_products_with_filter_after(self):
        
        logger.info("Test Case #7: Getting all products created after some specific date.")

        # Create data (date in the past should be changed to .iso format)
        x_days_from_today = 150
        after_created_date_not_isoformated = datetime.now().replace(microsecond=0) - timedelta(days=x_days_from_today)
        after_created_date = after_created_date_not_isoformated.isoformat()

        # Making an api call
        request_body = dict()
        request_body['after'] = after_created_date

        rs_with_all_fetched_products = ProductsHelper().call_list_products(request_body)
        assert rs_with_all_fetched_products, f"Empty response for 'list products with filter"

        # Get data from the db and verify actual response matches db records
        db_products = ProductsDAO().get_products_created_after_given_date(after_created_date)
        assert len(rs_with_all_fetched_products) == len(db_products), f"List products with filter 'after' returned unexpected number of products." \
                                                f"Expected: {len(db_products)}, Actual: {len(rs_with_all_fetched_products)}"

        logger.info("Fetched list of products matches actual list recorded in the db")

        # Verify a number of ids in the received list is matching the db list and list is not empty
        ids_in_api = [i['id'] for i in rs_with_all_fetched_products]
        ids_in_db = [i['ID'] for i in db_products]
        ids_diff = list(set(ids_in_api) - set(ids_in_db))
        assert not ids_diff, f"List products with filter, product ids in response mismatch in db."
