# -*- coding: utf-8 -*-
from urllib.parse import urljoin

import pytest
from rest_framework.status import HTTP_200_OK

import allure
from directory_tests_shared import URLs
from tests.smoke.cms_api_helpers import get_and_assert

pytestmark = [
    allure.suite("robots.txt"),
    allure.feature("robots.txt"),
    allure.description(
        "The HttpOnly flag should be set by including this attribute within "
        "the relevant Set-cookie directive. Alternatively, URL rewriting could be used,"
        " as is detailed in the following example"
    ),
]


@pytest.mark.parametrize(
    "url",
    [
        urljoin(URLs.DOMESTIC_LANDING.absolute, "robots.txt"),
        urljoin(URLs.EXOPPS_LANDING.absolute, "robots.txt"),
        urljoin(URLs.FAB_LANDING.absolute, "robots.txt"),
        urljoin(URLs.INTERNATIONAL_LANDING.absolute, "robots.txt"),
        urljoin(URLs.SOO_LANDING.absolute, "robots.txt"),
        urljoin(URLs.SSO_LANDING.absolute, "robots.txt"),
    ],
)
def test_robots_txt(url, basic_auth):
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)


@allure.issue("TT-1499", "Profile - doesn't have robots.txt")
@pytest.mark.skip(reason="see BUG TT-1499")
@pytest.mark.parametrize("url", [urljoin(URLs.PROFILE_LANDING.absolute, "robots.txt")])
def test_robots_txt_on_profile(url, basic_auth):
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)
