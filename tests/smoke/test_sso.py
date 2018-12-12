import http.client

import pytest

from tests import get_absolute_url


def test_legacy_api_health_check_endpoint_should_not_exist(logged_in_session, sso_hawk_cookie):
    url = get_absolute_url('sso:health')
    response = logged_in_session.get(
        url, allow_redirects=True, cookies=sso_hawk_cookie
    )
    assert response.status_code == 404


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
        logged_in_session, absolute_url, sso_hawk_cookie):
    response = logged_in_session.get(
        absolute_url, allow_redirects=True, cookies=sso_hawk_cookie
    )
    assert response.status_code == http.client.OK


@pytest.mark.parametrize("absolute_url, expected_status_code", [
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
        logged_in_session, absolute_url, expected_status_code, sso_hawk_cookie):
    # get rid of trailing slash
    if absolute_url[-1] == "/":
        absolute_url = absolute_url[:-1]
    response = logged_in_session.get(
        absolute_url, allow_redirects=False, cookies=sso_hawk_cookie
    )
    assert response.status_code == expected_status_code


@pytest.mark.dev
@pytest.mark.parametrize("absolute_url, expected_status_code", [
    (get_absolute_url('sso:landing'), http.client.FOUND),
])
def test_redirects_on_dev_after_removing_trailing_slash_as_logged_in_user(
        logged_in_session, absolute_url, expected_status_code, sso_hawk_cookie):
    # get rid of trailing slash
    if absolute_url[-1] == "/":
        absolute_url = absolute_url[:-1]
    response = logged_in_session.get(
        absolute_url, allow_redirects=False, cookies=sso_hawk_cookie
    )
    assert response.status_code == expected_status_code


@pytest.mark.stage
@pytest.mark.parametrize("absolute_url, expected_status_code", [
    (get_absolute_url('sso:landing'), http.client.MOVED_PERMANENTLY),
])
def test_redirects_on_stage_after_removing_trailing_slash_as_logged_in_user(
        logged_in_session, absolute_url, expected_status_code, sso_hawk_cookie):
    """
    Because STAGE is using path based routing the first redirect is 301
    instead of 302 like on DEV
    """
    # get rid of trailing slash
    if absolute_url[-1] == "/":
        absolute_url = absolute_url[:-1]
    response = logged_in_session.get(
        absolute_url, allow_redirects=False, cookies=sso_hawk_cookie
    )
    assert response.status_code == expected_status_code
