# -*- coding: utf-8 -*-
import pytest
from rest_framework.status import HTTP_200_OK, HTTP_302_FOUND

import allure
from directory_tests_shared import URLs
from tests.smoke.cms_api_helpers import get_and_assert

pytestmark = [allure.suite("Domestic site"), allure.feature("Domestic site")]


@pytest.mark.parametrize(
    "url",
    [
        URLs.DOMESTIC_LANDING_UK.absolute,
        URLs.DOMESTIC_INTERNATIONAL.absolute,
        URLs.DOMESTIC_INTERNATIONAL_UK.absolute,
        URLs.DOMESTIC_INTERNATIONAL_ZH.absolute,
        URLs.DOMESTIC_INTERNATIONAL_DE.absolute,
        URLs.DOMESTIC_INTERNATIONAL_JA.absolute,
        URLs.DOMESTIC_INTERNATIONAL_ES.absolute,
        URLs.DOMESTIC_INTERNATIONAL_PT.absolute,
        URLs.DOMESTIC_INTERNATIONAL_AR.absolute,
        URLs.DOMESTIC_TRIAGE_SECTOR.absolute,
        URLs.DOMESTIC_TRIAGE_EXPORTED_BEFORE.absolute,
        URLs.DOMESTIC_TRIAGE_REGULAR_EXPORTER.absolute,
        URLs.DOMESTIC_TRIAGE_ONLINE_MARKETPLACE.absolute,
        URLs.DOMESTIC_TRIAGE_COMPANIES_HOUSE.absolute,
        URLs.DOMESTIC_TRIAGE_COMPANY.absolute,
        URLs.DOMESTIC_TRIAGE_SUMMARY.absolute,
        URLs.DOMESTIC_CUSTOM.absolute,
        URLs.DOMESTIC_GET_FINANCE.absolute,
        URLs.DOMESTIC_STORY_FIRST.absolute,
        URLs.DOMESTIC_STORY_SECOND.absolute,
        URLs.DOMESTIC_TERMS.absolute,
        URLs.DOMESTIC_PRIVACY.absolute,
    ],
)
def test_domestic_pages(url, basic_auth):
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)


@pytest.mark.parametrize("url", [URLs.DOMESTIC_LANDING.absolute])
def test_domestic_home_page_might_redirect_to_international(url, basic_auth):
    response = get_and_assert(
        url=url, status_code=HTTP_200_OK, auth=basic_auth, allow_redirects=True
    )
    if response.history:
        last_redirect = response.history[-1]
        assert last_redirect.headers["location"] == "/international/?lang=en-gb"


@pytest.mark.parametrize(
    "url,redirect",
    [
        (URLs.DOMESTIC_NEW.absolute, "/advice/"),
        (URLs.DOMESTIC_OCCASIONAL.absolute, "/advice/"),
        (URLs.DOMESTIC_REGULAR.absolute, "/advice/"),
        (URLs.DOMESTIC_MARKET_RESEARCH.absolute, "/advice/find-an-export-market/"),
        (
            URLs.DOMESTIC_CUSTOMER_INSIGHT.absolute,
            "/advice/prepare-to-do-business-in-a-foreign-country/",
        ),
        (URLs.DOMESTIC_FINANCE.absolute, "/advice/get-export-finance-and-funding/"),
        (URLs.DOMESTIC_BUSINESS_PLANNING.absolute, "/advice/define-route-to-market/"),
        (
            URLs.DOMESTIC_GETTING_PAID.absolute,
            "/advice/manage-payment-for-export-orders/",
        ),
        (
            URLs.DOMESTIC_OPERATIONS_AND_COMPLIANCE.absolute,
            "/advice/manage-legal-and-ethical-compliance/",
        ),
    ],
)
def test_domestic_redirects(url, redirect, basic_auth):
    resp = get_and_assert(url=url, status_code=HTTP_302_FOUND, auth=basic_auth)
    location = resp.headers["location"]
    error = f"Expected redirect to '{redirect}' but got '{location}'"
    assert resp.headers["location"] == redirect, error
