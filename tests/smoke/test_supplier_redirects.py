# -*- coding: utf-8 -*-
import pytest
from rest_framework.status import HTTP_302_FOUND

import allure
from directory_tests_shared import URLs
from tests.smoke.cms_api_helpers import get_and_assert

pytestmark = [allure.suite("FAS redirects"), allure.feature("FAS redirects")]


@allure.issue("CMS-1834", "Links to legacy industry pages redirect to wrong place")
@allure.issue("ED-4152", "404s on old industry pages & contact-us page")
@pytest.mark.parametrize(
    "old_url,to_new_endpoint",
    [
        (
            URLs.FAS_INDUSTRIES_HEALTH.absolute,
            URLs.FAS_INCOMING_REDIRECT.absolute_template.format(
                endpoint="industries/health"
            ),
        ),
        (
            URLs.FAS_INDUSTRIES_TECH.absolute,
            URLs.FAS_INCOMING_REDIRECT.absolute_template.format(
                endpoint="industries/tech"
            ),
        ),
        (
            URLs.FAS_INDUSTRIES_CREATIVE.absolute,
            URLs.FAS_INCOMING_REDIRECT.absolute_template.format(
                endpoint="industries/creative"
            ),
        ),
    ],
)
def test_ed_4152_redirect_on_stage_from_old_industry_page(
    old_url, to_new_endpoint, basic_auth
):
    response = get_and_assert(
        url=old_url, status_code=HTTP_302_FOUND, auth=basic_auth, allow_redirects=False
    )

    error_msg = (
        f"Expected request to '{old_url}' to be redirected to "
        f"'{to_new_endpoint}' but instead it was redirected to "
        f"'{response.headers['Location']}'"
    )
    assert response.headers["Location"] == to_new_endpoint, error_msg
