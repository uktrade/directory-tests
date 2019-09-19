import uuid

from .settings import BASICAUTH_USER, BASICAUTH_PASS


def get_random_email_address():
    return "{}@example.com".format(uuid.uuid4())


def retriable_error(exception):
    """Return True if test should be re-run based on the Exception"""
    return isinstance(exception, (AssertionError, ))


def is_500(exception):
    """Return True exception message contains 500"""
    return "500" in str(exception)


def basic_auth():
    return BASICAUTH_USER, BASICAUTH_PASS
