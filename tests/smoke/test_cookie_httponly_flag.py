# -*- coding: utf-8 -*-
import pytest
from requests import Response
from rest_framework.status import HTTP_200_OK

import allure
from directory_tests_shared import URLs
from tests.smoke.cms_api_helpers import get_and_assert, status_error

pytestmark = [
    allure.suite("HttpOnly Cookie flag"),
    allure.feature("HttpOnly Cookie flag"),
    allure.description(
        "The HttpOnly flag should be set by including this attribute within "
        "the relevant Set-cookie directive. Alternatively, URL rewriting could be used,"
        " as is detailed in the following example"
    ),
]


@allure.step("Assert that HttpOnly Cookie flag is set")
def assert_httponly_cookie_flag_is_set(response: Response):
    without_httponly = {
        c.name: c.__dict__
        for c in response.cookies
        if not c.has_nonstandard_attr("HttpOnly")
    }
    error = (
        f"Following cookies on {response.url} are set without 'HttpOnly' flag: "
        f"{list(without_httponly.keys())} → {without_httponly}"
    )
    assert not list(without_httponly.keys()), error


@allure.issue("TT-1615", "Cookies Not Set With HttpOnly")
@pytest.mark.parametrize(
    "url",
    [
        URLs.FAB_CONFIRM_COMPANY_ADDRESS.absolute,
        URLs.FAB_CONFIRM_IDENTITY.absolute,
        URLs.FAB_CONFIRM_IDENTITY_LETTER.absolute,
        URLs.CONTACT_US_SOO_ORGANISATION_DETAILS.absolute,
        URLs.CONTACT_US_SOO_ORGANISATION_YOUR_EXPERIENCE.absolute,
        URLs.CONTACT_US_SOO_ORGANISATION_CONTACT_DETAILS.absolute,
        URLs.CONTACT_US_SOO_ORGANISATION_SUCCESS.absolute,
        URLs.EXOPPS_LANDING.absolute,
        URLs.PROFILE_LANDING.absolute,
        URLs.PROFILE_SOO.absolute,
        URLs.PROFILE_BUSINESS_PROFILE.absolute,
        URLs.PROFILE_EXOPS_ALERTS.absolute,
        URLs.PROFILE_EXOPS_APPLICATIONS.absolute,
        URLs.SSO_LOGOUT.absolute,
        URLs.SSO_PASSWORD_CHANGE.absolute,
        URLs.SSO_PASSWORD_SET.absolute,
        URLs.SSO_PASSWORD_RESET.absolute,
        URLs.SSO_EMAIL_CONFIRM.absolute,
        URLs.SSO_INACTIVE.absolute,
        URLs.CONTACT_US_SOO_ORGANISATION.absolute_template.format(market="eBay"),
    ],
)
def test_secure_cookie_flag_is_set_for_pages_behind_auth(
    url, basic_auth, logged_in_session
):
    response = logged_in_session.get(url, allow_redirects=True, auth=basic_auth)
    assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)
    assert_httponly_cookie_flag_is_set(response)


@allure.issue("TT-1615", "Cookies Not Set With HttpOnly")
@pytest.mark.parametrize(
    "url",
    [
        URLs.DOMESTIC_LANDING_UK.absolute,
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
        URLs.FAB_LANDING.absolute,
        URLs.FAS_LANDING.absolute,
        URLs.FAS_SEARCH.absolute,
        URLs.INTERNATIONAL_LANDING.absolute,
        URLs.INTERNATIONAL_REGIONS_MIDLANDS.absolute,
        URLs.INTERNATIONAL_REGIONS_NORTH_ENGLAND.absolute,
        URLs.INTERNATIONAL_REGIONS_NORTHERN_IRELAND.absolute,
        URLs.INTERNATIONAL_REGIONS_SOUTH_ENGLAND.absolute,
        URLs.INTERNATIONAL_REGIONS_WALES.absolute,
        URLs.INTERNATIONAL_INDUSTRY_AEROSPACE.absolute,
        URLs.INTERNATIONAL_INDUSTRY_AUTOMOTIVE.absolute,
        URLs.INTERNATIONAL_INDUSTRY_HEALTH_AND_LIFE_SCIENCES.absolute,
        URLs.INTERNATIONAL_INDUSTRY_TECHNOLOGY.absolute,
        URLs.INTERNATIONAL_INDUSTRY_FINANCIAL_SERVICES.absolute,
        URLs.INTERNATIONAL_INDUSTRY_CREATIVE_INDUSTRIES.absolute,
        URLs.SOO_LANDING.absolute,
        URLs.SOO_SEARCH_RESULTS.absolute,
        URLs.SOO_MARKETS_COUNT.absolute,
        URLs.SSO_LOGIN.absolute,
        URLs.CONTACT_US_LANDING.absolute,
    ],
)
def test_secure_cookie_flag_is_set_for_public_pages(url, basic_auth):
    response = get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)
    assert_httponly_cookie_flag_is_set(response)


@allure.issue("TT-1615", "Cookies Not Set With HttpOnly")
@pytest.mark.dev
@pytest.mark.parametrize(
    "url",
    [
        URLs.EXOPPS_LANDING.absolute,
        URLs.EXOPPS_SEARCH.absolute_template.format(term="food"),
        URLs.EXOPPS_OPPORTUNITY.absolute_template.format(slug="computer-equipment-783"),
    ],
)
def test_secure_cookie_flag_is_present_export_opportunities_dev(url, basic_auth):
    response = get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)
    assert_httponly_cookie_flag_is_set(response)


@allure.issue("TT-1615", "Cookies Not Set With HttpOnly")
@pytest.mark.stage
@pytest.mark.parametrize(
    "url",
    [
        URLs.EXOPPS_SEARCH.absolute_template.format(term="food"),
        URLs.EXOPPS_OPPORTUNITY.absolute_template.format(slug="furniture-498"),
    ],
)
def test_secure_cookie_flag_is_present_export_opportunities_stage(url, basic_auth):
    response = get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)
    assert_httponly_cookie_flag_is_set(response)


@allure.issue("TT-1615", "Cookies Not Set With HttpOnly")
@pytest.mark.dev
@pytest.mark.parametrize(
    "url",
    list(
        map(
            lambda name: URLs.SOO_MARKET_DETAILS.absolute_template.format(market=name),
            [
                "1688com",
                "amazon-canada",
                "amazon-france",
                "amazon-germany",
                "amazon-italy",
                "amazon-japan",
                "amazon-spain",
                "amazon-usa",
                "cdiscount",
                "ebay",
                "flipkart",
                "jd-worldwide",
                "kaola",
                "newegg-inc",
                "privalia",
                "rakuten",
                "royal-mail-t-mall",
                "spartoo",
                "trademe",
            ],
        )
    ),
)
def test_secure_cookie_flag_is_present_on_soo(url, basic_auth):
    response = get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)
    assert_httponly_cookie_flag_is_set(response)
