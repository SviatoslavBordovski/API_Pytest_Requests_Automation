from src.helpers.products_helper import ProductsHelper
from src.dao.products_dao import ProductsDAO
import pytest
from datetime import datetime, timedelta
import pdb

@pytest.mark.regression
class TestListProductsWithFilter(object):

    @pytest.mark.tc7
    def test_list_products_with_filter_after(self):

        # create data (date in the past changed to .iso format)
        x_days_from_today = 150
        after_created_date_not_isoformated = datetime.now().replace(microsecond=0) - timedelta(days=x_days_from_today)
        after_created_date = after_created_date_not_isoformated.isoformat()

        # making api call
        request_body = dict()
        request_body['after'] = after_created_date

        rs_api = ProductsHelper().call_list_products(request_body)
        pdb.set_trace()

        assert rs_api, f"Empty response for 'list products with filter"

        # get data from db
        db_products = ProductsDAO().get_products_created_after_given_date(after_created_date)

        # verify response match db
        assert len(rs_api) == len(db_products), f"List products with filter 'after' returned unexpected number of products." \
                                                f"Expected: {len(db_products)}, Actual: {len(rs_api)}"

        ids_in_api = [i['id'] for i in rs_api]
        ids_in_db = [i['ID'] for i in db_products]

        ids_diff = list(set(ids_in_api) - set(ids_in_db))
        assert not ids_diff, f"List products with filter, product ids in response mismatch in db."
