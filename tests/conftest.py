# -*- coding: utf-8 -*-
from typing import Tuple

import pytest
from requests import Session
from requests.auth import HTTPBasicAuth
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from directory_tests_shared import URLs
from directory_tests_shared.clients import (
    BASIC_AUTHENTICATOR,
    CMS_API_CLIENT,
    SSO_API_CLIENT,
)
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
def test_sso_user() -> dict:
    """Creates an unverified test SSO user.

    Such user won't have any business profile associated with it.
    It can be treated as a UK Tax payer account.

    :returns a dict with basic user details
    {
        'email': 'test+451359d7e7e644278cc66f4342c78741@directory.uktrade.digital',
        'password': 'password',
        'id': 34715,
        'first_name': 'Automated',
        'last_name': 'Test',
        'job_title': 'AUTOMATED TESTS',
        'mobile_phone_number': 1027958256750
    }
    """
    create_user_response = SSO_API_CLIENT.post(
        "/testapi/test-users/", data={}, authenticator=BASIC_AUTHENTICATOR
    )
    assert create_user_response.status_code == HTTP_200_OK
    return create_user_response.json()


@pytest.fixture
def test_sso_user_verified(test_sso_user) -> dict:
    """Creates a verified test SSO user.

    Such user won't have any business profile associated with it.
    It can be treated as a UK Tax payer account.
    """
    verify_response = SSO_API_CLIENT.patch(
        url=f"testapi/user-by-email/{test_sso_user['email']}/",
        data={"is_verified": True},
        authenticator=BASIC_AUTHENTICATOR,
    )
    assert verify_response.status_code == HTTP_204_NO_CONTENT
    return test_sso_user


@pytest.fixture
def session_and_csrf_middleware_token() -> Tuple[Session, str]:
    session = Session()
    login_url = URLs.SSO_LOGIN.absolute
    response = session.get(url=login_url, auth=(BASICAUTH_USER, BASICAUTH_PASS))
    assert (
        response.status_code == 200
    ), f"Expected 200 but got {response.status_code} from {response.url}"
    return session, extract_csrf_middleware_token(response.content.decode("UTF-8"))


@pytest.fixture
def logged_in_session_and_user(
    test_sso_user_verified: dict, session_and_csrf_middleware_token: Tuple[Session, str]
) -> Tuple[Session, dict]:
    session, csrfmiddlewaretoken = session_and_csrf_middleware_token
    data = {
        "login": test_sso_user_verified["email"],
        "password": test_sso_user_verified["password"],
        "csrfmiddlewaretoken": csrfmiddlewaretoken,
        "next": URLs.PROFILE_ABOUT.absolute,
    }
    response = session.post(
        url=URLs.SSO_LOGIN.absolute,
        data=data,
        allow_redirects=True,
        auth=(BASICAUTH_USER, BASICAUTH_PASS),
    )
    error = f"Expected 200 but got {response.status_code} from {response.url}"
    assert response.status_code == 200, error
    error = f"Couldn't find 'Sign out' in the response from: {response.url}"
    assert "Sign out" in response.content.decode("UTF-8"), error
    return session, test_sso_user_verified


@pytest.fixture
def logged_in_session(logged_in_session_and_user: Tuple[Session, dict]) -> Session:
    session, _ = logged_in_session_and_user
    return session
