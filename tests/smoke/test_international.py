# -*- coding: utf-8 -*-
import pytest
from rest_framework.status import HTTP_200_OK

import allure
from directory_tests_shared import URLs
from tests.smoke.cms_api_helpers import get_and_assert

pytestmark = [allure.suite("International site"), allure.feature("International site")]


@pytest.mark.dev
@pytest.mark.parametrize(
    "url",
    [
        URLs.INTERNATIONAL_REGIONS_MIDLANDS.absolute,
        URLs.INTERNATIONAL_REGIONS_NORTH_ENGLAND.absolute,
        URLs.INTERNATIONAL_REGIONS_NORTHERN_IRELAND.absolute,
        URLs.INTERNATIONAL_REGIONS_SOUTH_ENGLAND.absolute,
        URLs.INTERNATIONAL_REGIONS_WALES.absolute,
    ],
)
def test_region_pages(url, basic_auth):
    get_and_assert(
        url=url, status_code=HTTP_200_OK, auth=basic_auth, allow_redirects=True
    )


@pytest.mark.dev
@pytest.mark.parametrize(
    "url",
    [
        URLs.INTERNATIONAL_INDUSTRY_AEROSPACE.absolute,
        URLs.INTERNATIONAL_INDUSTRY_AUTOMOTIVE.absolute,
        URLs.INTERNATIONAL_INDUSTRY_CREATIVE_INDUSTRIES.absolute,
        URLs.INTERNATIONAL_INDUSTRY_EDUCATION.absolute,
        URLs.INTERNATIONAL_INDUSTRY_ENERGY.absolute,
        URLs.INTERNATIONAL_INDUSTRY_ENGINEERING_AND_MANUFACTURING.absolute,
        URLs.INTERNATIONAL_INDUSTRY_FINANCIAL_SERVICES.absolute,
        URLs.INTERNATIONAL_INDUSTRY_HEALTH_AND_LIFE_SCIENCES.absolute,
        URLs.INTERNATIONAL_INDUSTRY_LEGAL_SERVICES.absolute,
        URLs.INTERNATIONAL_INDUSTRY_REAL_ESTATE.absolute,
        URLs.INTERNATIONAL_INDUSTRY_SPACE.absolute,
        URLs.INTERNATIONAL_INDUSTRY_TECHNOLOGY.absolute,
    ],
)
def test_industry_pages_dev(url, basic_auth):
    get_and_assert(
        url=url, status_code=HTTP_200_OK, auth=basic_auth, allow_redirects=True
    )


@pytest.mark.stage
@pytest.mark.parametrize(
    "url",
    [
        URLs.INTERNATIONAL_INDUSTRY_CREATIVE_INDUSTRIES.absolute,
        URLs.INTERNATIONAL_INDUSTRY_ENERGY.absolute,
        URLs.INTERNATIONAL_INDUSTRY_ENGINEERING_AND_MANUFACTURING.absolute,
        URLs.INTERNATIONAL_INDUSTRY_FINANCIAL_AND_PROFESSIONAL_SERVICES.absolute,
        URLs.INTERNATIONAL_INDUSTRY_FINANCIAL_SERVICES.absolute,
        URLs.INTERNATIONAL_INDUSTRY_HEALTH_AND_LIFE_SCIENCES.absolute,
        URLs.INTERNATIONAL_INDUSTRY_LEGAL_SERVICES.absolute,
        URLs.INTERNATIONAL_INDUSTRY_REAL_ESTATE.absolute,
        URLs.INTERNATIONAL_INDUSTRY_TECHNOLOGY.absolute,
    ],
)
def test_industry_pages_stage(url, basic_auth):
    get_and_assert(
        url=url, status_code=HTTP_200_OK, auth=basic_auth, allow_redirects=True
    )


@pytest.mark.uat
@pytest.mark.parametrize(
    "url",
    [
        URLs.INTERNATIONAL_INDUSTRY_AEROSPACE.absolute,
        URLs.INTERNATIONAL_INDUSTRY_AGRICULTURAL_TECHNOLOGY.absolute,
        URLs.INTERNATIONAL_INDUSTRY_AUTOMOTIVE.absolute,
        URLs.INTERNATIONAL_INDUSTRY_CREATIVE_INDUSTRIES.absolute,
        URLs.INTERNATIONAL_INDUSTRY_CYBER_SECURITY.absolute,
        URLs.INTERNATIONAL_INDUSTRY_EDUCATION.absolute,
        URLs.INTERNATIONAL_INDUSTRY_ENGINEERING_AND_MANUFACTURING.absolute,
        URLs.INTERNATIONAL_INDUSTRY_FINANCIAL_SERVICES.absolute,
        URLs.INTERNATIONAL_INDUSTRY_FOOD_AND_DRINK.absolute,
        URLs.INTERNATIONAL_INDUSTRY_HEALTH_AND_LIFE_SCIENCES.absolute,
        URLs.INTERNATIONAL_INDUSTRY_LEGAL_SERVICES.absolute,
        URLs.INTERNATIONAL_INDUSTRY_MARITIME.absolute,
        URLs.INTERNATIONAL_INDUSTRY_NUCLEAR_ENERGY.absolute,
        URLs.INTERNATIONAL_INDUSTRY_OIL_AND_GAS.absolute,
        URLs.INTERNATIONAL_INDUSTRY_RETAIL.absolute,
        URLs.INTERNATIONAL_INDUSTRY_SPACE.absolute,
        URLs.INTERNATIONAL_INDUSTRY_SPORTS_ECONOMY.absolute,
        URLs.INTERNATIONAL_INDUSTRY_TECHNOLOGY.absolute,
    ],
)
def test_industry_pages_uat(url, basic_auth):
    get_and_assert(
        url=url, status_code=HTTP_200_OK, auth=basic_auth, allow_redirects=True
    )
