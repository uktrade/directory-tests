# -*- coding: utf-8 -*-
import pytest
import requests
from requests.auth import HTTPBasicAuth
from retrying import retry

from directory_tests_shared import URLs
from directory_tests_shared.clients import CMS_API_CLIENT
from directory_tests_shared.constants import USERS
from directory_tests_shared.settings import BASICAUTH_PASS, BASICAUTH_USER


@pytest.fixture
def cms_client():
    return CMS_API_CLIENT


@pytest.fixture
def basic_auth():
    return HTTPBasicAuth(BASICAUTH_USER, BASICAUTH_PASS)


def extract_csrf_middleware_token(content: str) -> str:
    line = [l for l in content.splitlines() if "csrfmiddlewaretoken" in l][0]
    delimiter = '"' if '"' in line else "'"
    fields = line.strip().split(delimiter)
    token_position = 5
    return fields[token_position]


@pytest.fixture
@retry(wait_fixed=5000, stop_max_attempt_number=2)
def logged_in_session():
    session = requests.Session()
    login_url = URLs.SSO_LOGIN.absolute
    response = session.get(url=login_url, auth=(BASICAUTH_USER, BASICAUTH_PASS))
    assert (
        response.status_code == 200
    ), f"Expected 200 but got {response.status_code} from {response.url}"
    csrfmiddlewaretoken = extract_csrf_middleware_token(
        response.content.decode("UTF-8")
    )
    user = USERS["verified"]
    data = {
        "login": user["username"],
        "password": user["password"],
        "csrfmiddlewaretoken": csrfmiddlewaretoken,
        "next": URLs.PROFILE_ABOUT.absolute,
    }
    response = session.post(
        url=login_url,
        data=data,
        allow_redirects=True,
        auth=(BASICAUTH_USER, BASICAUTH_PASS),
    )
    error = f"Expected 200 but got {response.status_code} from {response.url}"
    assert response.status_code == 200, error
    error = f"Couldn't find 'Sign out' in the response from: {response.url}"
    assert "Sign out" in response.content.decode("UTF-8"), error
    return session
