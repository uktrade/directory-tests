# -*- coding: utf-8 -*-
import pytest
import requests
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_301_MOVED_PERMANENTLY,
    HTTP_302_FOUND,
)

import allure
from directory_tests_shared import URLs
from tests.smoke.cms_api_helpers import get_and_assert, status_error

pytestmark = [
    allure.suite("Letter links"),
    allure.feature("Letter links"),
    allure.description(
        "Links to legacy pages which were used in physical letters sent to our users "
        "should redirect to appropriate new pages"
    ),
]


@pytest.mark.stage
@pytest.mark.parametrize(
    "url",
    [
        URLs.LEGACY_CONTACT_US_HELP.absolute,
        URLs.LEGACY_CONTACT_US_FEEDBACK_FORM.absolute,
    ],
)
def test_access_as_anon_user(url, basic_auth):
    response = requests.get(url, allow_redirects=False)
    redirect = response.headers["location"]
    get_and_assert(
        url=redirect, allow_redirects=True, status_code=HTTP_200_OK, auth=basic_auth
    )


@pytest.mark.stage
@pytest.mark.parametrize(
    "url",
    [
        URLs.LEGACY_CONTACT_US_HELP.absolute,
        URLs.LEGACY_CONTACT_US_FEEDBACK_FORM.absolute,
    ],
)
def test_access_contact_us_as_anon_user_after_removing_trailing_slash(url, basic_auth):
    # get rid of trailing slash
    if url[-1] == "/":
        url = url[:-1]
    response = requests.get(url, allow_redirects=False)
    redirect = response.headers["location"]
    get_and_assert(
        url=redirect, allow_redirects=True, status_code=HTTP_200_OK, auth=basic_auth
    )


@pytest.mark.stage
@pytest.mark.parametrize("url", [URLs.FAB_CONFIRM_IDENTITY.absolute])
def test_302_redirects_for_anon_user(url, basic_auth):
    get_and_assert(
        url=url, allow_redirects=False, status_code=HTTP_302_FOUND, auth=basic_auth
    )


@pytest.mark.parametrize("url", [URLs.FAB_CONFIRM_IDENTITY.absolute])
def test_301_redirects_after_removing_trailing_slash_for_anon_user(url, basic_auth):
    # get rid of trailing slash
    if url[-1] == "/":
        url = url[:-1]
    response = get_and_assert(
        url=url,
        allow_redirects=False,
        status_code=HTTP_301_MOVED_PERMANENTLY,
        auth=basic_auth,
    )
    assert response.headers["location"] == "/find-a-buyer/verify/"


@pytest.mark.session_auth
@pytest.mark.stage
@pytest.mark.parametrize("url", [URLs.FAB_CONFIRM_IDENTITY.absolute])
def test_access_endpoints_as_logged_in_user(logged_in_session, url, basic_auth):
    response = logged_in_session.get(url, allow_redirects=True, auth=basic_auth)
    assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)


@pytest.mark.session_auth
@pytest.mark.stage
@pytest.mark.parametrize("url", [URLs.FAB_CONFIRM_IDENTITY.absolute])
def test_check_if_verify_endpoint_redirects_to_correct_page(
    logged_in_session, url, basic_auth
):
    response = logged_in_session.get(url, allow_redirects=True, auth=basic_auth)
    assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)
    # final redirect depends on the account's verification status
    # for a verified profile request should be redirected to /profile/find-a-buyer/
    # and for an unverified profile it should go to /find-a-buyer/verify/letter-confirm/
    got_to_letter_confirmation = (
        response.url == URLs.FAB_CONFIRM_COMPANY_ADDRESS.absolute
    )
    got_to_profile = response.url == URLs.PROFILE_BUSINESS_PROFILE.absolute
    error = (
        f"Expected request to {url} to be redirected to "
        f"{URLs.FAB_CONFIRM_COMPANY_ADDRESS.absolute} or {URLs.PROFILE_BUSINESS_PROFILE.absolute} "
        f"but got to {response.url}"
    )
    assert got_to_letter_confirmation or got_to_profile, error


@pytest.mark.parametrize("url", [URLs.FAB_CONFIRM_IDENTITY.absolute])
def test_anonymous_request_to_verify_endpoint_redirects_to_login_page(url, basic_auth):
    response = requests.get(url, allow_redirects=True, auth=basic_auth)
    assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)
    expected_url = URLs.SSO_LOGIN.absolute_template.format(next="/find-a-buyer/verify/")
    error = (
        f"Expected request to {url} to be redirected to "
        f"{expected_url} but was redirected to {response.url}"
    )
    assert response.url == expected_url, error
