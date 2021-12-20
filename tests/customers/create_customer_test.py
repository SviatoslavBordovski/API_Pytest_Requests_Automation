import pytest
import logging as logger
from src.helpers.customers_helper import CustomerHelper
from src.utilities.genericUtilities import generate_random_email_and_password
from src.dao.customers_dao import CustomersDAO
from src.utilities.requestsUtility import RequestsUtility

@pytest.mark.customers
@pytest.mark.tc1
def test_create_customer_only_email_password():
    logger.info("Test Case #1: create new customer with email only.")

    rand_info = generate_random_email_and_password()
    generated_email = rand_info['email']
    generated_password = rand_info['password']

    # make the 'post' request/call
    cust_obj = CustomerHelper()
    cust_api_info = cust_obj.create_customer(email=generated_email, password=generated_password)

    # Verify email and first name in the response
    assert cust_api_info['email'] == generated_email, f"Create customer api return wrong email. Email: {generated_email}"
    assert cust_api_info['first_name'] == '', f"Create customer api returned value for first_name" \
                                              f"but it should be empty. "

    logger.info("Email and first name are verified, so new customer has been created")

    # verify customer is created in database
    cust_dao = CustomersDAO()
    cust_info = cust_dao.get_customer_by_email(generated_email)

    id_in_api = cust_api_info['id']
    id_in_db = cust_info[0]['ID']
    assert id_in_api == id_in_db, f'Create customer response "id" not same as "ID" in database.' \
                                  f'Email: {generated_email}'

@pytest.mark.customers
@pytest.mark.tc2
def test_create_customer_fail_for_existing_email():

    logger.info("Test Case #2: get existing customer from the db and reject creation new customer with the same email")

    # get user's existing email from db
    cust_dao = CustomersDAO()
    existing_customer = cust_dao.get_random_customer_from_db()
    existing_email = existing_customer[0]['user_email']

    # call the api
    req_helper = RequestsUtility()
    request_body = {"email": existing_email, "password": "Password1"}
    cust_api_info = req_helper.post(endpoint='customers', body_params=request_body, expected_status_code=400)

    assert cust_api_info['code'] == 'registration-error-email-exists', f"You are trying " \
        f"with existing email, this is why you are getting 'code' status code error. Expected" \
        f" to see 'registration-error-email-exists' but found '{cust_api_info['code']}' status code."

    assert cust_api_info['message'] == 'An account is already registered with your email address. ' \
        '<a href="#" class="showlogin">Please log in.</a>', \
        f"Such account was already registered, so user exists. Expected to see: " \
        f"'An account is already registered with your email address. <a href='#' class='showlogin'>Please log in.</a>'" \
        f" message but for some reason found '{cust_api_info['message']}' message instead."

    logger.info("New user creation with existing email address is restricted. All good.")
