# -*- coding: utf-8 -*-
import pytest
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_301_MOVED_PERMANENTLY,
    HTTP_302_FOUND,
)
from retrying import retry

import allure
from directory_tests_shared import URLs
from directory_tests_shared.utils import is_500
from tests.smoke.cms_api_helpers import get_and_assert, status_error

pytestmark = [allure.suite("Profile"), allure.feature("Profile")]


def test_about_200(basic_auth):
    url = URLs.PROFILE_ABOUT.absolute
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)


@allure.issue("TT-1298", "This url returns 500 ISE")
@pytest.mark.skip(reason="BUG TT-1298 - this url returns 500 ISE")
@pytest.mark.parametrize("url", [URLs.PROFILE_COMPANY_EDIT_SOCIAL_MEDIA.absolute])
def test_302_redirects_for_anon_user_bug_tt_1298(url, basic_auth):
    get_and_assert(url=url, status_code=HTTP_302_FOUND, auth=basic_auth)


@pytest.mark.parametrize(
    "url",
    [
        URLs.PROFILE_LANDING.absolute,
        URLs.PROFILE_SOO.absolute,
        URLs.PROFILE_BUSINESS_PROFILE.absolute,
        URLs.PROFILE_EXOPS_ALERTS.absolute,
        URLs.PROFILE_EXOPS_APPLICATIONS.absolute,
    ],
)
def test_302_redirects_for_anon_user(url, basic_auth):
    get_and_assert(url=url, status_code=HTTP_302_FOUND, auth=basic_auth)


@pytest.mark.parametrize(
    "url",
    [
        URLs.PROFILE_SOO.absolute,
        URLs.PROFILE_BUSINESS_PROFILE.absolute,
        URLs.PROFILE_EXOPS_ALERTS.absolute,
        URLs.PROFILE_EXOPS_APPLICATIONS.absolute,
    ],
)
def test_301_redirects_after_removing_trailing_slash_for_anon_user(url, basic_auth):
    # get rid of trailing slash
    if url[-1] == "/":
        url = url[:-1]
    get_and_assert(url=url, status_code=HTTP_301_MOVED_PERMANENTLY, auth=basic_auth)


@pytest.mark.session_auth
@retry(wait_fixed=3000, stop_max_attempt_number=2, retry_on_exception=is_500)
@pytest.mark.parametrize(
    "url",
    [
        URLs.PROFILE_LANDING.absolute,
        URLs.PROFILE_SOO.absolute,
        URLs.PROFILE_BUSINESS_PROFILE.absolute,
        URLs.PROFILE_EXOPS_ALERTS.absolute,
        URLs.PROFILE_EXOPS_APPLICATIONS.absolute,
    ],
)
def test_access_to_non_health_check_endpoints_as_logged_in_user(
    logged_in_session, url, basic_auth
):
    response = logged_in_session.get(url, allow_redirects=True, auth=basic_auth)
    assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)
