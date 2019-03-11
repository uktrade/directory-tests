from tests.settings import BASICAUTH_USER, BASICAUTH_PASS

USER_AGENT = {"User-Agent": "locust - load tests"}


def basic_auth():
    return BASICAUTH_USER, BASICAUTH_PASS
