from rest_framework.status import *

import pytest

from tests import get_absolute_url
from tests.smoke.cms_api_helpers import status_error


@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('sso:landing'),
    get_absolute_url('sso:login'),
    get_absolute_url('sso:signup'),
])
def test_access_sso_endpoints_as_logged_in_user_w_redirect_to_sud(
        logged_in_session, absolute_url, hawk_cookie):
    response = logged_in_session.get(
        absolute_url, allow_redirects=True, cookies=hawk_cookie
    )
    assert response.status_code == HTTP_200_OK, status_error(
        HTTP_200_OK, response
    )


@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('sso:logout'),
    get_absolute_url('sso:password_change'),
    get_absolute_url('sso:password_set'),
    get_absolute_url('sso:password_reset'),
    get_absolute_url('sso:email_confirm'),
    get_absolute_url('sso:inactive'),
])
def test_access_sso_endpoints_as_logged_in_user_wo_redirect_to_sud(
        logged_in_session, absolute_url, hawk_cookie):
    response = logged_in_session.get(
        absolute_url, allow_redirects=True, cookies=hawk_cookie
    )
    assert response.status_code == HTTP_200_OK, status_error(
        HTTP_200_OK, response
    )


@pytest.mark.parametrize("absolute_url, expected_status_code", [
    (get_absolute_url('sso:landing'), HTTP_301_MOVED_PERMANENTLY),
    (get_absolute_url('sso:login'), HTTP_301_MOVED_PERMANENTLY),
    (get_absolute_url('sso:signup'), HTTP_301_MOVED_PERMANENTLY),
    (get_absolute_url('sso:logout'), HTTP_301_MOVED_PERMANENTLY),
    (get_absolute_url('sso:password_change'), HTTP_301_MOVED_PERMANENTLY),
    (get_absolute_url('sso:password_set'), HTTP_301_MOVED_PERMANENTLY),
    (get_absolute_url('sso:password_reset'), HTTP_301_MOVED_PERMANENTLY),
    (get_absolute_url('sso:email_confirm'), HTTP_301_MOVED_PERMANENTLY),
    (get_absolute_url('sso:inactive'), HTTP_301_MOVED_PERMANENTLY),
])
def test_redirects_after_removing_trailing_slash_as_logged_in_user(
        logged_in_session, absolute_url, expected_status_code, hawk_cookie):
    # get rid of trailing slash
    if absolute_url[-1] == "/":
        absolute_url = absolute_url[:-1]
    response = logged_in_session.get(
        absolute_url, allow_redirects=False, cookies=hawk_cookie
    )


@pytest.mark.dev
@pytest.mark.parametrize("absolute_url, expected_status_code", [
    (get_absolute_url('sso:landing'), http.client.FOUND),
])
def test_redirects_on_dev_after_removing_trailing_slash_as_logged_in_user(
        logged_in_session, absolute_url, expected_status_code, hawk_cookie):
    # get rid of trailing slash
    if absolute_url[-1] == "/":
        absolute_url = absolute_url[:-1]
    response = logged_in_session.get(
        absolute_url, allow_redirects=False, cookies=hawk_cookie
    )
    assert response.status_code == expected_status_code


@pytest.mark.stage
@pytest.mark.parametrize("absolute_url, expected_status_code", [
    (get_absolute_url('sso:landing'), http.client.MOVED_PERMANENTLY),
])
def test_redirects_on_stage_after_removing_trailing_slash_as_logged_in_user(
        logged_in_session, absolute_url, expected_status_code, hawk_cookie):
    """
    Because STAGE is using path based routing the first redirect is 301
    instead of 302 like on DEV
    """
    # get rid of trailing slash
    if absolute_url[-1] == "/":
        absolute_url = absolute_url[:-1]
    response = logged_in_session.get(
        absolute_url, allow_redirects=False, cookies=hawk_cookie
    )
    assert response.status_code == expected_status_code, status_error(
        expected_status_code, response
    )
