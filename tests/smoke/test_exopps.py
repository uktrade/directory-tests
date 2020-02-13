# -*- coding: utf-8 -*-
import pytest
from rest_framework.status import HTTP_200_OK

import allure
from directory_tests_shared import URLs
from tests.smoke.cms_api_helpers import get_and_assert

pytestmark = [
    allure.suite("Export Opportunities"),
    allure.feature("Export Opportunities"),
]


@pytest.mark.parametrize(
    "url",
    [
        URLs.EXOPPS_LANDING.absolute,
        URLs.EXOPPS_OPPORTUNITY.absolute_template.format(slug="furniture-498"),
        URLs.EXOPPS_SEARCH.absolute_template.format(term="food"),
    ],
)
def test_exopps_pages(url, basic_auth):
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)
