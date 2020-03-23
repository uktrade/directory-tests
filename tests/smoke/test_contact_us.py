# -*- coding: utf-8 -*-
import pytest
from rest_framework.status import HTTP_200_OK

import allure
from directory_tests_shared import URLs
from tests.smoke.cms_api_helpers import get_and_assert

pytestmark = [allure.suite("Contact us"), allure.feature("Contact us")]


@pytest.mark.dev
@pytest.mark.parametrize(
    "market",
    [
        "1688com",
        "amazon-canada",
        "amazon-china",
        "amazon-france",
        "amazon-germany",
        "amazon-italy",
        "amazon-japan",
        "amazon-spain",
        "amazon-usa",
        "cdiscount",
        "ebay",
        "etsy",
        "flipkart",
        "jd-worldwide",
        "kaola",
        "newegg-inc",
        "privalia",
        "rakuten",
        "royal-mail-t-mall",
        "sfbest",
        "shangpin",
        "spartoo",
        "trademe",
    ],
)
def test_access_contact_us_organisation_endpoints_dev(market, basic_auth):
    params = {"market": market}
    get_and_assert(
        url=URLs.CONTACT_US_SOO_ORGANISATION.absolute,
        params=params,
        allow_redirects=True,
        status_code=HTTP_200_OK,
        auth=basic_auth,
    )


@pytest.mark.stage
@pytest.mark.parametrize(
    "market",
    [
        "1688com",
        "amazon-canada",
        "amazon-china",
        "amazon-france",
        "amazon-germany",
        "amazon-italy",
        "amazon-japan",
        "amazon-mexico",
        "amazon-spain",
        "amazon-usa",
        "cdiscount",
        "ebay",
        "flipkart",
        "fruugo",
        "goxip",
        "jd-worldwide",
        "kaola",
        "la-redoute",
        "linio",
        "newegg-business",
        "newegg-canada",
        "newegg-inc",
        "privalia",
        "rakuten",
        "royal-mail-t-mall",
        "sfbest",
        "shangpin",
        "spartoo",
        "trademe",
        "tthigo",
    ],
)
def test_access_contact_us_organisation_endpoints_stage(market, basic_auth):
    params = {"market": market}
    get_and_assert(
        url=URLs.CONTACT_US_SOO_ORGANISATION.absolute,
        params=params,
        allow_redirects=True,
        status_code=HTTP_200_OK,
        auth=basic_auth,
    )


@pytest.mark.prod
@pytest.mark.parametrize(
    "market",
    [
        "1688com",
        "amazon-canada",
        "amazon-china",
        "amazon-france",
        "amazon-germany",
        "amazon-italy",
        "amazon-japan",
        "amazon-mexico",
        "amazon-spain",
        "amazon-usa",
        "bol",
        "catch",
        "cdiscount",
        "darty",
        "ebay",
        "eprice",
        "flipkart",
        "fnac",
        "fruugo",
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
        "royal-mail-t-mall",
        "sfbest",
        "shangpin",
        "spartoo",
        "trademe",
        "tthigo",
    ],
)
def test_access_contact_us_organisation_endpoints_prod(market):
    params = {"market": market}
    get_and_assert(
        url=URLs.CONTACT_US_SOO_ORGANISATION.absolute,
        params=params,
        allow_redirects=True,
        status_code=HTTP_200_OK,
    )


@pytest.mark.parametrize(
    "url",
    [
        URLs.CONTACT_US_SOO_ORGANISATION_DETAILS.absolute,
        URLs.CONTACT_US_SOO_ORGANISATION_YOUR_EXPERIENCE.absolute,
        URLs.CONTACT_US_SOO_ORGANISATION_CONTACT_DETAILS.absolute,
        URLs.CONTACT_US_SOO_ORGANISATION_SUCCESS.absolute,
    ],
)
def test_access_contact_us_endpoints(url, basic_auth):
    get_and_assert(
        url=url, allow_redirects=True, status_code=HTTP_200_OK, auth=basic_auth
    )
