import http.client

import pytest
import requests

from tests import get_absolute_url
from tests.settings import DIRECTORY_API_HEALTH_CHECK_TOKEN as TOKEN


def test_health_check_database():
    params = {'token': TOKEN}
    response = requests.get(
            get_absolute_url('sso:healthcheck-database'), params=params)
    assert response.status_code == http.client.OK


def test_legacy_api_health_check_endpoint_should_not_exist(logged_in_session):
    url = get_absolute_url('sso:health')
    response = logged_in_session.get(url, allow_redirects=True)
    assert response.status_code == 404


    assert response.status_code == http.client.OK


def test_invalid_sso_authorization_sessionid(logged_in_session):
    url = get_absolute_url('sso:user')
    headers = {"Authorization": "SSO_SESSION_ID invalid_sessionid"}
    response = logged_in_session.get(url, headers=headers, allow_redirects=True)
    assert response.status_code == 403


def test_missing_sso_authorization_sessionid(logged_in_session):
    url = get_absolute_url('sso:user')
    response = logged_in_session.get(url, allow_redirects=True)
    assert response.status_code == 403


@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('sso:landing'),
    get_absolute_url('sso:login'),
    get_absolute_url('sso:signup'),
    get_absolute_url('sso:logout'),
    get_absolute_url('sso:password_change'),
    get_absolute_url('sso:password_set'),
    get_absolute_url('sso:password_reset'),
    get_absolute_url('sso:email_confirm'),
    get_absolute_url('sso:inactive'),
])
def test_access_sso_endpoints_as_logged_in_user(
        logged_in_session, absolute_url):
    response = logged_in_session.get(absolute_url, allow_redirects=True)
    assert response.status_code == http.client.OK


@pytest.mark.parametrize("absolute_url, expected_status_code", [
    (get_absolute_url('sso:landing'), http.client.FOUND),
    (get_absolute_url('sso:login'), http.client.MOVED_PERMANENTLY),
    (get_absolute_url('sso:signup'), http.client.MOVED_PERMANENTLY),
    (get_absolute_url('sso:logout'), http.client.MOVED_PERMANENTLY),
    (get_absolute_url('sso:password_change'), http.client.MOVED_PERMANENTLY),
    (get_absolute_url('sso:password_set'), http.client.MOVED_PERMANENTLY),
    (get_absolute_url('sso:password_reset'), http.client.MOVED_PERMANENTLY),
    (get_absolute_url('sso:email_confirm'), http.client.MOVED_PERMANENTLY),
    (get_absolute_url('sso:inactive'), http.client.MOVED_PERMANENTLY),
])
def test_redirects_after_removing_trailing_slash_as_logged_in_user(
        logged_in_session, absolute_url, expected_status_code):
    # get rid of trailing slash
    if absolute_url[-1] == "/":
        absolute_url = absolute_url[:-1]
    response = logged_in_session.get(absolute_url, allow_redirects=False)
    assert response.status_code == expected_status_code
