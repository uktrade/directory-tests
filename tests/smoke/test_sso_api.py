# -*- coding: utf-8 -*-
import datetime

import pytest
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

import allure
from directory_tests_shared.clients import BASIC_AUTHENTICATOR, SSO_API_CLIENT
from directory_tests_shared.constants import USERS
from tests.smoke.cms_api_helpers import status_error

pytestmark = [allure.suite("SSO-API"), allure.feature("SSO-API")]


@allure.description(
    "This test gets the user_session_id from currently logged in session and then uses "
    "'URLs.SSO_API_USER' endpoint ('api/v1/session-user/') to get user details"
)
@pytest.mark.dev
@pytest.mark.session_auth
def test_sso_authentication_using_api_client(logged_in_session):
    user_session_id = logged_in_session.cookies.get("directory_sso_dev_session")

    response = SSO_API_CLIENT.user.get_session_user(
        session_id=user_session_id, authenticator=BASIC_AUTHENTICATOR
    )

    assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)
    assert "Access Denied" not in response.content.decode("UTF-8")


@allure.description(
    "This test gets the user_session_id from currently logged in session and then uses "
    "'URLs.SSO_API_USER' endpoint ('api/v1/session-user/') to get user details"
)
@pytest.mark.stage
@pytest.mark.session_auth
def test_sso_authentication_using_api_client_and_stage_cookie(logged_in_session):
    user_session_id = logged_in_session.cookies.get("sso_stage_session")

    response = SSO_API_CLIENT.user.get_session_user(
        session_id=user_session_id, authenticator=BASIC_AUTHENTICATOR
    )

    assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)
    assert "Access Denied" not in response.content.decode("UTF-8")


@allure.issue("TT-856", "IP restriction was added to 'oauth2/' endpoints")
@pytest.mark.skip(reason="see TT-856")
def test_get_oauth2_user_profile():
    token = USERS["verified"]["token"]
    response = SSO_API_CLIENT.user.get_oauth2_user_profile(bearer_token=token)
    assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)
    assert "Access Denied" not in response.content.decode("UTF-8")


@allure.issue("TT-856", "IP restriction was added to 'oauth2/' endpoints")
@pytest.mark.skip(reason="see TT-856")
@pytest.mark.parametrize("token", ["", "invalid_token", None])
def test_get_oauth2_user_profile_w_invalid_token(token):
    response = SSO_API_CLIENT.user.get_oauth2_user_profile(bearer_token=token)
    assert response.status_code == HTTP_401_UNAUTHORIZED, status_error(
        HTTP_401_UNAUTHORIZED, response
    )
    assert "Access Denied" not in response.content.decode("UTF-8")


@pytest.mark.dev
@pytest.mark.session_auth
def test_check_password_using_dev_cookie(logged_in_session_and_user):
    session, user = logged_in_session_and_user
    user_session_id = session.cookies.get("directory_sso_dev_session")
    assert user_session_id
    password = user["password"]
    response = SSO_API_CLIENT.user.check_password(
        user_session_id, password, authenticator=BASIC_AUTHENTICATOR
    )
    assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)
    assert "Access Denied" not in response.content.decode("UTF-8")


@pytest.mark.stage
@pytest.mark.session_auth
def test_check_password_using_stage_cookie(logged_in_session_and_user):
    session, user = logged_in_session_and_user
    user_session_id = session.cookies.get("sso_stage_session")
    assert user_session_id
    password = user["password"]
    response = SSO_API_CLIENT.user.check_password(
        user_session_id, password, authenticator=BASIC_AUTHENTICATOR
    )
    assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)
    assert "Access Denied" not in response.content.decode("UTF-8")


@pytest.mark.session_auth
@pytest.mark.parametrize("password", ["", "invalid_password", None])
def test_check_invalid_password(logged_in_session, password):
    user_session_id = logged_in_session.cookies.get("directory_sso_dev_session")
    response = SSO_API_CLIENT.user.check_password(
        user_session_id, password, authenticator=BASIC_AUTHENTICATOR
    )
    assert response.status_code == HTTP_400_BAD_REQUEST, status_error(
        HTTP_400_BAD_REQUEST, response
    )
    assert "Access Denied" not in response.content.decode("UTF-8")


def test_get_all_login_dates():
    response = SSO_API_CLIENT.user.get_last_login(authenticator=BASIC_AUTHENTICATOR)
    assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)
    assert "Access Denied" not in response.content.decode("UTF-8")


def test_get_login_dates_since_today():
    today = str(datetime.date.today())
    response = SSO_API_CLIENT.user.get_last_login(
        start=today, authenticator=BASIC_AUTHENTICATOR
    )
    assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)
    assert "Access Denied" not in response.content.decode("UTF-8")
