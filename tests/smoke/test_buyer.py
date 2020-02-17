# -*- coding: utf-8 -*-
from urllib.parse import urljoin

import pytest
import requests
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_301_MOVED_PERMANENTLY,
    HTTP_302_FOUND,
    HTTP_404_NOT_FOUND,
)

import allure
from directory_tests_shared import URLs
from directory_tests_shared.constants import COMPANIES
from tests.smoke.cms_api_helpers import get_and_assert, status_error

pytestmark = [allure.suite("FAB"), allure.feature("FAB")]


@allure.issue("ED-3188", "ATM we're not caching inactive companies: see ED-3188")
@allure.issue("ED-3782", "ATM we're not caching inactive companies: see ED-3782")
@pytest.mark.skip(
    reason="ATM we're not caching inactive companies: see tickets: ED-3188, ED-3782"
)
def test_landing_page_post_company_not_active(basic_auth):
    data = {"company_number": COMPANIES["not_active"]}
    response = requests.post(
        URLs.FAB_LANDING.absolute, data=data, allow_redirects=False, auth=basic_auth
    )
    assert "Company not active" in str(response.content)


@allure.title("We should get 404 Not Found for a nonexistent page")
@pytest.mark.session_auth
@pytest.mark.parametrize("url", [urljoin(URLs.FAB_LANDING.absolute, "foobar")])
def test_not_existing_page_return_404_user(logged_in_session, basic_auth, url):
    response = logged_in_session.get(url, allow_redirects=False, auth=basic_auth)
    assert response.status_code == HTTP_404_NOT_FOUND, status_error(
        HTTP_404_NOT_FOUND, response
    )


@allure.title("Requests to certain URLs without trailing slash should be redirected")
@allure.link(
    "TT-1543", "Missing redirect to enrolment page for legacy /find-a-buyer/register/"
)
@pytest.mark.parametrize(
    "url,destination", [(URLs.FAB_REGISTER.absolute, URLs.PROFILE_ENROL.absolute)]
)
def test_redirects_to_profile_pages(url, destination, basic_auth):
    # get rid of trailing slash -> see TT-1543
    if url[-1] == "/":
        url = url[:-1]
    response = get_and_assert(
        url=url, allow_redirects=False, status_code=HTTP_302_FOUND, auth=basic_auth
    )
    location = response.headers["location"]
    error = (
        f"Expected '{url}' to return a redirect which would get us to "
        f"'{destination}' but got redirect to '{location}'"
    )
    assert destination.endswith(location), error


@allure.story(
    "Anonymous requests to Company & Identity confirmation pages should be redirected "
    "with 302 Found"
)
@pytest.mark.parametrize(
    "url",
    [
        URLs.FAB_CONFIRM_COMPANY_ADDRESS.absolute,
        URLs.FAB_CONFIRM_IDENTITY.absolute,
        URLs.FAB_CONFIRM_IDENTITY_LETTER.absolute,
    ],
)
def test_302_redirects_for_anon_user(url, basic_auth):
    get_and_assert(
        url=url, allow_redirects=False, status_code=HTTP_302_FOUND, auth=basic_auth
    )


@allure.story(
    "Anonymous requests to Company & Identity confirmation pages (without trailing "
    "slash) should be redirected with 301 Moved Permanently"
)
@pytest.mark.parametrize(
    "url",
    [
        URLs.FAB_CONFIRM_COMPANY_ADDRESS.absolute,
        URLs.FAB_CONFIRM_IDENTITY.absolute,
        URLs.FAB_CONFIRM_IDENTITY_LETTER.absolute,
    ],
)
def test_301_redirects_after_removing_trailing_slash_for_anon_user(url, basic_auth):
    # get rid of trailing slash
    if url[-1] == "/":
        url = url[:-1]
    get_and_assert(
        url=url,
        allow_redirects=False,
        status_code=HTTP_301_MOVED_PERMANENTLY,
        auth=basic_auth,
    )


@allure.story(
    "Authenticated requests to Company & Identity confirmation pages should not be "
    "redirected"
)
@pytest.mark.session_auth
@pytest.mark.parametrize(
    "url",
    [
        URLs.FAB_LANDING.absolute,
        URLs.FAB_CONFIRM_COMPANY_ADDRESS.absolute,
        URLs.FAB_CONFIRM_IDENTITY.absolute,
        URLs.FAB_CONFIRM_IDENTITY_LETTER.absolute,
    ],
)
def test_access_non_health_check_endpoints_as_logged_in_user(
    url, logged_in_session, basic_auth
):
    response = logged_in_session.get(url, allow_redirects=True, auth=basic_auth)
    assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)
