import datetime
import pytest
from rest_framework.status import *

from directory_sso_api_client.client import sso_api_client

from tests import users
from tests.smoke.cms_api_helpers import status_error


@pytest.mark.dev
@pytest.mark.session_auth
def test_sso_authentication_using_api_client(logged_in_session):
    """This test gets the user_session_id from currently logged in session
    and then uses SSO API "sso-api:user" endpoint ("api/v1/session-user/")
    to get user details
    """
    user_session_id = logged_in_session.cookies.get("directory_sso_dev_session")

    response = sso_api_client.user.get_session_user(session_id=user_session_id)

    assert response.status_code == HTTP_200_OK, status_error(
        HTTP_200_OK, response
    )


@pytest.mark.stage
@pytest.mark.session_auth
def test_sso_authentication_using_api_client_and_stage_cookie(logged_in_session):
    """This test gets the user_session_id from currently logged in session
    and then uses SSO API "sso-api:user" endpoint ("api/v1/session-user/")
    to get user details
    """
    user_session_id = logged_in_session.cookies.get("sso_stage_session")

    response = sso_api_client.user.get_session_user(session_id=user_session_id)

    assert response.status_code == HTTP_200_OK, status_error(
        HTTP_200_OK, response
    )


@pytest.mark.skip(reason="see TT-856")
def test_get_oauth2_user_profile():
    token = users["verified"]["token"]
    response = sso_api_client.user.get_oauth2_user_profile(bearer_token=token)
    assert response.status_code == HTTP_200_OK, status_error(
        HTTP_200_OK, response
    )


@pytest.mark.skip(reason="see TT-856")
@pytest.mark.parametrize("token", [
    "",
    "invalid_token",
    None,
])
def test_get_oauth2_user_profile_w_invalid_token(token):
    response = sso_api_client.user.get_oauth2_user_profile(bearer_token=token)
    assert response.status_code == HTTP_401_UNAUTHORIZED, status_error(
        HTTP_200_OK, response
    )


@pytest.mark.dev
@pytest.mark.session_auth
def test_check_password_using_dev_cookie(logged_in_session):
    user_session_id = logged_in_session.cookies.get("directory_sso_dev_session")
    password = users["verified"]["password"]
    response = sso_api_client.user.check_password(user_session_id, password)
    assert response.status_code == HTTP_200_OK, status_error(
        HTTP_200_OK, response
    )


@pytest.mark.stage
@pytest.mark.session_auth
def test_check_password_using_stage_cookie(logged_in_session):
    user_session_id = logged_in_session.cookies.get("sso_stage_session")
    password = users["verified"]["password"]
    response = sso_api_client.user.check_password(user_session_id, password)
    assert response.status_code == HTTP_200_OK, status_error(
        HTTP_200_OK, response
    )


@pytest.mark.session_auth
@pytest.mark.parametrize("password", [
    "",
    "invalid_password",
    None,
])
def test_check_invalid_password(logged_in_session, password):
    user_session_id = logged_in_session.cookies.get("directory_sso_dev_session")
    response = sso_api_client.user.check_password(user_session_id, password)
    assert response.status_code == HTTP_400_BAD_REQUEST, status_error(
        HTTP_200_OK, response
    )


def test_get_all_login_dates():
    response = sso_api_client.user.get_last_login()
    assert response.status_code == HTTP_200_OK, status_error(
        HTTP_200_OK, response
    )


def test_get_login_dates_since_today():
    today = str(datetime.date.today())
    response = sso_api_client.user.get_last_login(start=today)
    assert response.status_code == HTTP_200_OK, status_error(
        HTTP_200_OK, response
    )
