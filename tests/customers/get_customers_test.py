import pytest
from src.utilities.requestsUtility import RequestsUtility

@pytest.mark.customers
@pytest.mark.tc3
def test_get_all_customers():

    req_helper = RequestsUtility()
    rs_api = req_helper.get(endpoint='customers')

    assert rs_api, f"Response of a list with all customers is empty."
