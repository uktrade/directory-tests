import datetime
import http.client

import pytest
import requests

from tests import get_absolute_url, users
from tests.settings import DIRECTORY_API_HEALTH_CHECK_TOKEN as TOKEN


@pytest.mark.session_auth
def test_health_check_database():
    """This endpoint still uses session auth instead of HAWK signature check"""
    params = {'token': TOKEN}
    response = requests.get(
            get_absolute_url('sso-api:healthcheck-database'), params=params)
    assert response.status_code == http.client.OK


@pytest.mark.hawk
def test_health_check_ping(sso_api_client):
    """Uses HAWK signature check"""
    response = sso_api_client.ping()
    assert response.status_code == http.client.OK


@pytest.mark.session_auth
@pytest.mark.hawk
def test_sso_authentication_using_api_client(logged_in_session, sso_api_client):
    """This test gets the user_session_id from currently logged in session
    and then uses SSO API 'sso-api:user' endpoint ('api/v1/session-user/')
    to get user details
    """
    user_session_id = logged_in_session.cookies.get("directory_sso_dev_session")

    response = sso_api_client.user.get_session_user(session_id=user_session_id)

    assert response.status_code == http.client.OK


@pytest.mark.hawk
def test_get_oauth2_user_profile(sso_api_client):
    token = users['verified']['token']
    response = sso_api_client.user.get_oauth2_user_profile(bearer_token=token)
    assert response.status_code == http.client.OK


@pytest.mark.hawk
@pytest.mark.parametrize("token", [
    "",
    "invalid_token",
    None,
])
def test_get_oauth2_user_profile_w_invalid_token(sso_api_client, token):
    response = sso_api_client.user.get_oauth2_user_profile(bearer_token=token)
    assert response.status_code == 401


@pytest.mark.hawk
def test_check_password(logged_in_session, sso_api_client):
    user_session_id = logged_in_session.cookies.get("directory_sso_dev_session")
    password = users['verified']['password']
    response = sso_api_client.user.check_password(user_session_id, password)
    assert response.status_code == http.client.OK


@pytest.mark.hawk
@pytest.mark.parametrize("password", [
    "",
    "invalid_password",
    None,
])
def test_check_invalid_password(logged_in_session, sso_api_client, password):
    user_session_id = logged_in_session.cookies.get("directory_sso_dev_session")
    response = sso_api_client.user.check_password(user_session_id, password)
    assert response.status_code == 400


@pytest.mark.hawk
def test_get_all_login_dates(sso_api_client):
    response = sso_api_client.user.get_last_login()
    assert response.status_code == http.client.OK


@pytest.mark.hawk
def test_get_login_dates_since_today(sso_api_client):
    today = str(datetime.date.today())
    response = sso_api_client.user.get_last_login(start=today)
    assert response.status_code == http.client.OK
