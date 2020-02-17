# -*- coding: utf-8 -*-
import pytest
from rest_framework.status import HTTP_200_OK, HTTP_301_MOVED_PERMANENTLY

import allure
from directory_tests_shared import URLs
from tests.smoke.cms_api_helpers import get_and_assert, status_error

pytestmark = [allure.suite("SSO"), allure.feature("SSO")]


@pytest.mark.session_auth
@pytest.mark.parametrize(
    "url",
    [URLs.SSO_LANDING.absolute, URLs.SSO_LOGIN.absolute, URLs.SSO_SIGNUP.absolute],
)
def test_access_sso_endpoints_as_logged_in_user_w_redirect_to_sud(
    logged_in_session, url, basic_auth
):
    response = logged_in_session.get(url, allow_redirects=True, auth=basic_auth)
    assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)


@pytest.mark.prod
@pytest.mark.parametrize(
    "url",
    [
        URLs.SSO_LOGOUT.absolute,
        URLs.SSO_PASSWORD_CHANGE.absolute,
        URLs.SSO_PASSWORD_SET.absolute,
        URLs.SSO_PASSWORD_RESET.absolute,
        URLs.SSO_EMAIL_CONFIRM.absolute,
        URLs.SSO_INACTIVE.absolute,
    ],
)
def test_access_sso_endpoints_as_anonymous_user_yields_200(url, basic_auth):
    get_and_assert(
        url=url, allow_redirects=True, status_code=HTTP_200_OK, auth=basic_auth
    )


@allure.issue("TT-1758", "500 ISE on sso/accounts/password/change/")
@pytest.mark.session_auth
@pytest.mark.parametrize(
    "url",
    [
        URLs.SSO_LOGOUT.absolute,
        URLs.SSO_PASSWORD_CHANGE.absolute,
        URLs.SSO_PASSWORD_SET.absolute,
        URLs.SSO_PASSWORD_RESET.absolute,
        URLs.SSO_EMAIL_CONFIRM.absolute,
        URLs.SSO_INACTIVE.absolute,
    ],
)
def test_access_sso_endpoints_as_logged_in_user_without_redirect_to_sud(
    logged_in_session, url, basic_auth
):
    response = logged_in_session.get(url, allow_redirects=True, auth=basic_auth)
    assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)


@pytest.mark.session_auth
@pytest.mark.parametrize(
    "url, expected_status_code",
    [
        (URLs.SSO_LOGIN.absolute, HTTP_301_MOVED_PERMANENTLY),
        (URLs.SSO_SIGNUP.absolute, HTTP_301_MOVED_PERMANENTLY),
        (URLs.SSO_LOGOUT.absolute, HTTP_301_MOVED_PERMANENTLY),
        (URLs.SSO_PASSWORD_CHANGE.absolute, HTTP_301_MOVED_PERMANENTLY),
        (URLs.SSO_PASSWORD_SET.absolute, HTTP_301_MOVED_PERMANENTLY),
        (URLs.SSO_PASSWORD_RESET.absolute, HTTP_301_MOVED_PERMANENTLY),
        (URLs.SSO_EMAIL_CONFIRM.absolute, HTTP_301_MOVED_PERMANENTLY),
        (URLs.SSO_INACTIVE.absolute, HTTP_301_MOVED_PERMANENTLY),
    ],
)
def test_redirects_after_removing_trailing_slash_as_logged_in_user(
    logged_in_session, url, expected_status_code, basic_auth
):
    # get rid of trailing slash
    if url[-1] == "/":
        url = url[:-1]
    response = logged_in_session.get(url, allow_redirects=False, auth=basic_auth)
    assert response.status_code == expected_status_code, status_error(
        expected_status_code, response
    )


@allure.issue(
    "TT-2287",
    "TT-2287 going to /sso without trailing slash redirects to not existent /sso/sso/ page",
)
@pytest.mark.dev
@pytest.mark.prod
@pytest.mark.session_auth
@pytest.mark.parametrize(
    "url, expected_status_code",
    [(URLs.SSO_LANDING.absolute, HTTP_301_MOVED_PERMANENTLY)],
)
def test_redirects_after_removing_trailing_slash_as_logged_in_user_tt_2287(
    logged_in_session, url, expected_status_code, basic_auth
):
    # get rid of trailing slash
    if url[-1] == "/":
        url = url[:-1]
    response = logged_in_session.get(url, allow_redirects=False, auth=basic_auth)
    assert response.status_code == expected_status_code, status_error(
        expected_status_code, response
    )
