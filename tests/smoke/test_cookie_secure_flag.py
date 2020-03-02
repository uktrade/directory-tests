# -*- coding: utf-8 -*-
import pytest
from requests import Response
from rest_framework.status import HTTP_200_OK

import allure
from directory_tests_shared import URLs
from tests.smoke.cms_api_helpers import get_and_assert, status_error

pytestmark = [
    allure.suite("Secure Cookie flag"),
    allure.feature("Secure Cookie flag"),
    allure.description(
        "The Secure flag should be set on all cookies that are used for transmitting "
        "sensitive data when accessing content over HTTPS. If cookies are used to "
        "transmit session"
    ),
]


@allure.step("Assert that Secure Cookie flag is set")
def assert_secure_cookie_flag_is_set(response: Response):
    cookie_dict = {c.name: c.__dict__ for c in response.cookies}
    insecure_cookies = [c.name for c in response.cookies if not c.secure]
    error = (
        f"Not all cookies on {response.url} are set with 'Secure' flag: "
        f"{insecure_cookies} → {cookie_dict}"
    )
    assert all(c.secure for c in response.cookies), error


@allure.issue("TT-1614", "Cookies Not Set With Secure Flag")
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
    assert_secure_cookie_flag_is_set(response)


@allure.issue("TT-1614", "Cookies Not Set With Secure Flag")
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
        URLs.INTERNATIONAL_INDUSTRY_CREATIVE_INDUSTRIES.absolute,
        URLs.INTERNATIONAL_INDUSTRY_ENERGY.absolute,
        URLs.INTERNATIONAL_INDUSTRY_ENGINEERING_AND_MANUFACTURING.absolute,
        URLs.INTERNATIONAL_INDUSTRY_TECHNOLOGY.absolute,
        URLs.SSO_LOGIN.absolute,
        URLs.CONTACT_US_LANDING.absolute,
    ],
)
def test_secure_cookie_flag_is_set_for_public_pages(url, basic_auth):
    response = get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)
    assert_secure_cookie_flag_is_set(response)


@allure.issue("TT-1614", "Cookies Not Set With Secure Flag")
@allure.issue("XOT-1313", "XOT-1313 - SOO - secure cookie is not set in Dev & Staging")
@pytest.mark.skip(reason="SOO - secure cookie is not set in Dev & Staging: XOT-1313")
@pytest.mark.parametrize(
    "url",
    [
        URLs.SOO_LANDING.absolute,
        URLs.SOO_SEARCH_RESULTS.absolute,
        URLs.SOO_MARKETS_COUNT.absolute,
    ],
)
def test_secure_cookie_flag_is_set_for_public_pages_on_soo(url, basic_auth):
    response = get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)
    assert_secure_cookie_flag_is_set(response)


@allure.issue("TT-1614", "Cookies Not Set With Secure Flag")
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
    assert_secure_cookie_flag_is_set(response)


@allure.issue("TT-1614", "Cookies Not Set With Secure Flag")
@pytest.mark.stage
@pytest.mark.parametrize(
    "url",
    [
        URLs.EXOPPS_SEARCH.absolute_template.format(term="food"),
        URLs.EXOPPS_OPPORTUNITY.absolute_template.format(slug="furniture-917"),
    ],
)
def test_secure_cookie_flag_is_present_export_opportunities_stage(url, basic_auth):
    response = get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)
    assert_secure_cookie_flag_is_set(response)


@allure.issue("TT-1614", "Cookies Not Set With Secure Flag")
@allure.issue("XOT-1313", "XOT-1313 - SOO - secure cookie is not set in Dev & Staging")
@pytest.mark.dev
@pytest.mark.skip(reason="SOO - secure cookie is not set in Dev & Staging: XOT-1313")
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
def test_secure_cookie_flag_is_present_on_soo_dev(url, basic_auth):
    response = get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)
    assert_secure_cookie_flag_is_set(response)


@allure.issue("TT-1614", "Cookies Not Set With Secure Flag")
@allure.issue("XOT-1313", "XOT-1313 - SOO - secure cookie is not set in Dev & Staging")
@pytest.mark.stage
@pytest.mark.skip(reason="SOO - secure cookie is not set in Dev & Staging: XOT-1313")
@pytest.mark.parametrize(
    "url",
    list(
        map(
            lambda name: URLs.SOO_MARKET_DETAILS.absolute_template.format(market=name),
            [
                "goxip",
                "jd-worldwide",
                "kaola",
                "la-redoute",
                "linio",
                "mano-mano",
                "newegg-business",
                "newegg-canada",
                "newegg-inc",
                "onbuy",
                "privalia",
                "rakuten",
                "realde",
                "royal-mail-t-mall",
                "spartoo",
                "themarket",
                "trademe",
                "tthigo",
            ],
        )
    ),
)
def test_secure_cookie_flag_is_present_on_soo_stage(url, basic_auth):
    response = get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)
    assert_secure_cookie_flag_is_set(response)
