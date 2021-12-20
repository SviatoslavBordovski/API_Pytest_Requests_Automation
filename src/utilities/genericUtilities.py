import random
import logging as logger
import string

def generate_random_email_and_password(domain=None, email_prefix=None):
    logger.debug("Generating random email and password.")

    # Set domain and email prefix for email generation
    if not domain:
        domain = 'bordovski.pp.ua'
    if not email_prefix:
        email_prefix = 'testuser'

    # Set conditions for email generation
    random_email_string_length = 10
    random_string = ''.join(random.choices(string.ascii_lowercase, k=random_email_string_length))
    email = email_prefix + '_' + random_string + '@' + domain

    # Set conditions for password generation
    password_length = 15
    password_string = ''.join(random.choices(string.ascii_letters, k=password_length))
    password = password_string + '2022' + '_for_' + email_prefix + '_' + random_string + '@' + domain

    # Dictionary for credentials
    random_info = {'email': email, 'password': password}
    logger.debug(f"Randomly generated email and password: {random_info}")

    return random_info

def generate_random_string(length=10, prefix=None, suffix=None):

    random_string = ''.join(random.choices(string.ascii_lowercase, k=length))

    if prefix:
        random_string = prefix + random_string
    if suffix:
        random_string = random_string + suffix

    return random_string

def generate_random_coupon_code(sufix=None, length=10):

    code = ''.join(random.choices(string.ascii_uppercase, k=length))
    if sufix:
        code += sufix

    return code
