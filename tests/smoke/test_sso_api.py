import datetime
import http.client

import pytest
import requests
from directory_sso_api_client.client import sso_api_client
from tests import get_absolute_url, users
from tests.settings import DIRECTORY_API_HEALTH_CHECK_TOKEN as TOKEN


@pytest.mark.session_auth
@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('sso-api:healthcheck-database'),
    get_absolute_url('sso-api:healthcheck-ping'),
    get_absolute_url('sso-api:healthcheck-sentry'),
])
def test_health_check_database(absolute_url):
    """This endpoint still uses session auth instead of HAWK signature check"""
    params = {'token': TOKEN}
    response = requests.get(absolute_url, params=params)
    assert response.status_code == http.client.OK


@pytest.mark.hawk
def test_health_check_ping():
    """Uses HAWK signature check"""
    response = sso_api_client.ping()
    assert response.status_code == http.client.OK


@pytest.mark.dev
@pytest.mark.session_auth
@pytest.mark.hawk
def test_sso_authentication_using_api_client(logged_in_session):
    """This test gets the user_session_id from currently logged in session
    and then uses SSO API 'sso-api:user' endpoint ('api/v1/session-user/')
    to get user details
    """
    user_session_id = logged_in_session.cookies.get("directory_sso_dev_session")

    response = sso_api_client.user.get_session_user(session_id=user_session_id)

    assert response.status_code == http.client.OK


@pytest.mark.stage
@pytest.mark.session_auth
@pytest.mark.hawk
def test_sso_authentication_using_api_client_and_stage_cookie(logged_in_session):
    """This test gets the user_session_id from currently logged in session
    and then uses SSO API 'sso-api:user' endpoint ('api/v1/session-user/')
    to get user details
    """
    user_session_id = logged_in_session.cookies.get("sso_stage_session")

    response = sso_api_client.user.get_session_user(session_id=user_session_id)

    assert response.status_code == http.client.OK


@pytest.mark.hawk
def test_get_oauth2_user_profile(sso_hawk_cookie):
    token = users['verified']['token']
    response = sso_api_client.user.get_oauth2_user_profile(bearer_token=token, cookies=sso_hawk_cookie)
    assert response.status_code == http.client.OK


@pytest.mark.hawk
@pytest.mark.parametrize("token", [
    "",
    "invalid_token",
    None,
])
def test_get_oauth2_user_profile_w_invalid_token(token, sso_hawk_cookie):
    response = sso_api_client.user.get_oauth2_user_profile(bearer_token=token, cookies=sso_hawk_cookie)
    assert response.status_code == 401


@pytest.mark.dev
@pytest.mark.hawk
def test_check_password(logged_in_session):
    user_session_id = logged_in_session.cookies.get("directory_sso_dev_session")
    password = users['verified']['password']
    response = sso_api_client.user.check_password(user_session_id, password)
    assert response.status_code == http.client.OK


@pytest.mark.stage
@pytest.mark.hawk
def test_check_password_using_stage_cookie(logged_in_session):
    user_session_id = logged_in_session.cookies.get("sso_stage_session")
    password = users['verified']['password']
    response = sso_api_client.user.check_password(user_session_id, password)
    assert response.status_code == http.client.OK


@pytest.mark.hawk
@pytest.mark.parametrize("password", [
    "",
    "invalid_password",
    None,
])
def test_check_invalid_password(logged_in_session, password):
    user_session_id = logged_in_session.cookies.get("directory_sso_dev_session")
    response = sso_api_client.user.check_password(user_session_id, password)
    assert response.status_code == 400


@pytest.mark.hawk
def test_get_all_login_dates():
    response = sso_api_client.user.get_last_login()
    assert response.status_code == http.client.OK


@pytest.mark.hawk
def test_get_login_dates_since_today():
    today = str(datetime.date.today())
    response = sso_api_client.user.get_last_login(start=today)
    assert response.status_code == http.client.OK
