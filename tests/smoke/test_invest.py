from urllib.parse import urljoin

import pytest
from rest_framework.status import *

from tests import URLs
from tests.smoke.cms_api_helpers import get_and_assert


@pytest.mark.dev
@pytest.mark.parametrize(
    "url",
    [
        URLs.INVEST_INDUSTRIES_AEROSPACE.absolute,
        URLs.INVEST_INDUSTRIES_AUTOMOTIVE.absolute,
        URLs.INVEST_INDUSTRIES_CREATIVE_INDUSTRIES.absolute,
        URLs.INVEST_INDUSTRIES_HEALTH_AND_LIFE_SCIENCES.absolute,
        URLs.INVEST_INDUSTRIES_TECHNOLOGY.absolute,
    ],
)
def test_invest_pages_redirects(url, basic_auth):
    response = get_and_assert(url=url, status_code=HTTP_302_FOUND, auth=basic_auth, allow_redirects=False)
    location = response.headers["location"]
    error = f"Expected redirect to https://... URL but got {location}"
    assert location.startswith("https://"), error


@pytest.mark.dev
@pytest.mark.parametrize(
    "url,redirected",
    [
        (URLs.INVEST_INDUSTRIES.absolute, URLs.INTERNATIONAL_INDUSTRIES.absolute),
        (URLs.INVEST_INDUSTRIES_AEROSPACE.absolute, URLs.INTERNATIONAL_INDUSTRY_AEROSPACE.absolute),
        (URLs.INVEST_INDUSTRIES_AUTOMOTIVE.absolute, URLs.INTERNATIONAL_INDUSTRY_AUTOMOTIVE.absolute),
        (URLs.INVEST_INDUSTRIES_HEALTH_AND_LIFE_SCIENCES.absolute, URLs.INTERNATIONAL_INDUSTRY_HEALTH_AND_LIFE_SCIENCES.absolute),
        (URLs.INVEST_INDUSTRIES_TECHNOLOGY.absolute, URLs.INTERNATIONAL_INDUSTRY_TECHNOLOGY.absolute),
        # (URLs.INVEST_INDUSTRIES_CREATIVE_INDUSTRIES.absolute, URLs.INTERNATIONAL_INDUSTRY_CREATIVE_INDUSTRIES.absolute),
        # (URLs.INVEST_UK_SETUP_GUIDE.absolute, URLs.INTERNATIONAL_UK_SETUP_GUIDE.absolute),
    ],
)
def test_invest_pages_redirect_to_international_dev(url, redirected, basic_auth):
    response = get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth, allow_redirects=True)
    error = f"Expected {url} to redirect to {redirected} instead got to {response.url}"
    assert response.url == redirected, error


@pytest.mark.stage
@pytest.mark.parametrize(
    "url,redirected",
    [
        (URLs.INVEST_INDUSTRIES.absolute, URLs.INTERNATIONAL_INDUSTRIES.absolute),
        (URLs.INVEST_INDUSTRIES_TECHNOLOGY.absolute, URLs.INTERNATIONAL_INDUSTRY_TECHNOLOGY.absolute),
        # (URLs.INVEST_INDUSTRIES_AEROSPACE.absolute, URLs.INTERNATIONAL_INDUSTRY_AEROSPACE.absolute),
        # (URLs.INVEST_INDUSTRIES_AUTOMOTIVE.absolute, URLs.INTERNATIONAL_INDUSTRY_AUTOMOTIVE.absolute),
        # (URLs.INVEST_INDUSTRIES_HEALTH_AND_LIFE_SCIENCES.absolute, URLs.INTERNATIONAL_INDUSTRY_HEALTH_AND_LIFE_SCIENCES.absolute),
        # (URLs.INVEST_UK_SETUP_GUIDE.absolute, URLs.INTERNATIONAL_UK_SETUP_GUIDE.absolute),
        # (URLs.INVEST_INDUSTRIES_CREATIVE_INDUSTRIES.absolute, URLs.INTERNATIONAL_INDUSTRY_CREATIVE_INDUSTRIES.absolute),
    ],
)
def test_invest_pages_redirect_to_international_stage(url, redirected, basic_auth):
    response = get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth, allow_redirects=True)
    error = f"Expected {url} to redirect to {redirected} instead got to {response.url}"
    assert response.url == redirected, error


@pytest.mark.prod
@pytest.mark.parametrize(
    "url,redirected",
    [
        # These pages are present on Production but redirects are set to Invest Landing page
        # (URLs.INVEST_UK_SETUP_GUIDE.absolute, URLs.INTERNATIONAL_UK_SETUP_GUIDE.absolute),
        # (URLs.INVEST_UK_SETUP_GUIDE_ESTABLISH_A_BASE.absolute, URLs.INTERNATIONAL_UK_SETUP_GUIDE_ESTABLISH_A_BASE.absolute),
        # (URLs.INVEST_UK_SETUP_GUIDE_HIRE_SKILLED_WORKERS.absolute, URLs.INTERNATIONAL_UK_SETUP_GUIDE_ESTABLISH_A_BASE.absolute),
        # (URLs.INVEST_UK_SETUP_GUIDE_OPEN_BANK_ACCOUNT.absolute, URLs.INTERNATIONAL_UK_SETUP_GUIDE_OPEN_BANK_ACCOUNT.absolute),
        # (URLs.INVEST_UK_SETUP_GUIDE_REGISTER_A_COMPANY.absolute, URLs.INTERNATIONAL_UK_SETUP_GUIDE_REGISTER_A_COMPANY.absolute),
        # (URLs.INVEST_UK_SETUP_GUIDE_UK_TAX.absolute, URLs.INTERNATIONAL_UK_SETUP_GUIDE_UK_TAX.absolute),
        # (URLs.INVEST_UK_SETUP_GUIDE_UK_VISAS.absolute, URLs.INTERNATIONAL_UK_SETUP_GUIDE_UK_VISAS.absolute),

        (URLs.INVEST_REGIONS_LONDON.absolute, URLs.INTERNATIONAL_REGIONS_LONDON.absolute),
        (URLs.INVEST_REGIONS_MIDLANDS.absolute, URLs.INTERNATIONAL_REGIONS_MIDLANDS.absolute),
        (URLs.INVEST_REGIONS_NORTH_ENGLAND.absolute, URLs.INTERNATIONAL_REGIONS_NORTH_ENGLAND.absolute),
        (URLs.INVEST_REGIONS_NORTHERN_IRELAND.absolute, URLs.INTERNATIONAL_REGIONS_NORTHERN_IRELAND.absolute),
        (URLs.INVEST_REGIONS_SCOTLAND.absolute, URLs.INTERNATIONAL_REGIONS_SCOTLAND.absolute),
        (URLs.INVEST_REGIONS_SOUTH_ENGLAND.absolute, URLs.INTERNATIONAL_REGIONS_SOUTH_ENGLAND.absolute),
        (URLs.INVEST_REGIONS_WALES.absolute, URLs.INTERNATIONAL_REGIONS_WALES.absolute),

        (URLs.INVEST_INDUSTRIES.absolute, URLs.INTERNATIONAL_INDUSTRIES.absolute),
        # (URLs.INVEST_INDUSTRIES_ADVANCED_MANUFACTURING.absolute, URLs.INTERNATIONAL_INDUSTRY_ADVANCED_MANUFACTURING.absolute),
        (URLs.INVEST_INDUSTRIES_AEROSPACE.absolute, URLs.INTERNATIONAL_INDUSTRY_AEROSPACE.absolute),
        (URLs.INVEST_INDUSTRIES_AGRI_TECH.absolute, URLs.INTERNATIONAL_INDUSTRY_AGRICULTURAL_TECHNOLOGY.absolute),
        (URLs.INVEST_INDUSTRIES_AUTOMOTIVE.absolute, URLs.INTERNATIONAL_INDUSTRY_AUTOMOTIVE.absolute),
        (URLs.INVEST_INDUSTRIES_CAPITAL_INVESTMENT.absolute, URLs.INTERNATIONAL_CAPITAL_INVEST.absolute),
        # (URLs.INVEST_INDUSTRIES_CHEMICALS.absolute, URLs.INTERNATIONAL_INDUSTRY_CHEMICALS.absolute),
        # (URLs.INVEST_INDUSTRIES_CREATIVE_INDUSTRIES.absolute, URLs.INTERNATIONAL_INDUSTRY_CREATIVE_INDUSTRIES.absolute),
        # (URLs.INVEST_INDUSTRIES_ENERGY.absolute, URLs.INTERNATIONAL_INDUSTRY_ENERGY.absolute),
        (URLs.INVEST_INDUSTRIES_FINANCIAL_SERVICES.absolute, URLs.INTERNATIONAL_INDUSTRY_FINANCIAL_SERVICES.absolute),
        (URLs.INVEST_INDUSTRIES_FOOD_AND_DRINK.absolute, URLs.INTERNATIONAL_INDUSTRY_FOOD_AND_DRINK.absolute),
        (URLs.INVEST_INDUSTRIES_HEALTH_AND_LIFE_SCIENCES.absolute, URLs.INTERNATIONAL_INDUSTRY_HEALTH_AND_LIFE_SCIENCES.absolute),
        (URLs.INVEST_INDUSTRIES_RETAIL.absolute, URLs.INTERNATIONAL_INDUSTRY_RETAIL.absolute),
        (URLs.INVEST_INDUSTRIES_TECHNOLOGY.absolute, URLs.INTERNATIONAL_INDUSTRY_TECHNOLOGY.absolute),
    ],
)
def test_invest_pages_redirect_to_international_prod(url, redirected, basic_auth):
    response = get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth, allow_redirects=True)
    error = f"Expected {url} to redirect to {redirected} instead got to {response.url}"
    assert response.url == redirected, error


@pytest.mark.parametrize(
    "url",
    [
        URLs.INVEST_LANDING.absolute,
        URLs.INVEST_CONTACT.absolute,
        URLs.INVEST_INDUSTRIES.absolute,
        URLs.INVEST_HPO_CONTACT.absolute,
        URLs.INVEST_HPO_FOOD.absolute,
        URLs.INVEST_HPO_LIGHTWEIGHT.absolute,
        URLs.INVEST_HPO_RAIL.absolute,
        URLs.INVEST_INDUSTRIES_ADVANCED_MANUFACTURING.absolute,
        URLs.INVEST_INDUSTRIES_AGRI_TECH.absolute,
        URLs.INVEST_INDUSTRIES_ASSET_MANAGEMENT.absolute,
        URLs.INVEST_INDUSTRIES_AUTOMOTIVE_RESEARCH_AND_DEVELOPMENT.absolute,
        URLs.INVEST_INDUSTRIES_AUTOMOTIVE_SUPPLY_CHAIN.absolute,
        URLs.INVEST_INDUSTRIES_CAPITAL_INVESTMENT.absolute,
        URLs.INVEST_INDUSTRIES_CHEMICALS.absolute,
        URLs.INVEST_INDUSTRIES_CREATIVE_CONTENT_AND_PRODUCTION.absolute,
        URLs.INVEST_INDUSTRIES_DATA_ANALYTICS.absolute,
        URLs.INVEST_INDUSTRIES_DIGITAL_MEDIA.absolute,
        URLs.INVEST_INDUSTRIES_ELECTRICAL_NETWORKS.absolute,
        URLs.INVEST_INDUSTRIES_ENERGY.absolute,
        URLs.INVEST_INDUSTRIES_ENERGY_WASTE.absolute,
        URLs.INVEST_INDUSTRIES_FINANCIAL_TECHNOLOGY.absolute,
        URLs.INVEST_INDUSTRIES_FOOD_AND_DRINK.absolute,
        URLs.INVEST_INDUSTRIES_FOOD_SERVICE_AND_CATERING.absolute,
        URLs.INVEST_INDUSTRIES_FREE_FOODS.absolute,
        URLs.INVEST_INDUSTRIES_MEAT_POULTRY_AND_DAIRY.absolute,
        URLs.INVEST_INDUSTRIES_MEDICAL_TECHNOLOGY.absolute,
        URLs.INVEST_INDUSTRIES_MOTORSPORT.absolute,
        URLs.INVEST_INDUSTRIES_NUCLEAR_ENERGY.absolute,
        URLs.INVEST_INDUSTRIES_OFFSHORE_WIND_ENERGY.absolute,
        URLs.INVEST_INDUSTRIES_OIL_AND_GAS.absolute,
        URLs.INVEST_INDUSTRIES_PHARMACEUTICAL_MANUFACTURING.absolute,
        URLs.INVEST_INDUSTRIES_RETAIL.absolute,
    ],
)
def test_invest_pages(url, basic_auth):
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)


@pytest.mark.stage
@pytest.mark.parametrize(
    "endpoint",
    [
        URLs.INVEST_INDUSTRIES_FINANCIAL_SERVICES.relative,
    ],
)
def test_cms_918_redirect_to_international_if_matching_industry_exists(
    endpoint, basic_auth
):
    """
    A redirect to the International site will happen only if there’s a sector
    page with the same slug in International.
    """
    old_url = urljoin(URLs.INVEST_LANDING.absolute, endpoint)
    new_url = urljoin(URLs.INTERNATIONAL_LANDING.absolute, endpoint)
    response = get_and_assert(
        url=old_url,
        allow_redirects=False,
        status_code=HTTP_302_FOUND,
        auth=basic_auth,
    )

    error_msg = (
        f"Expected request to '{old_url}' to be redirected to "
        f"'{new_url}' but instead it was redirected to "
        f"'{response.headers['Location']}'"
    )
    assert response.headers["Location"] == new_url, error_msg


@pytest.mark.skip(
    reason="these International Industry pages aren't present yet"
)
@pytest.mark.stage
@pytest.mark.parametrize(
    "endpoint",
    [
        "industries/pharmaceutical-manufacturing/",
        "industries/medical-technology/",
        "industries/creative-industries/",
        "industries/digital-media/",
        "industries/creative-content-and-production/",
        "industries/food-and-drink/",
        "industries/meat-poultry-and-dairy/",
        "industries/food-service-and-catering/",
        "industries/free-foods/",
        "industries/asset-management/",
        "industries/financial-technology/",
        "industries/agri-tech/",
        "industries/retail/",
        "industries/chemicals/",
        "industries/technology/",
        "industries/data-analytics/",
        "industries/capital-investment/",
        "industries/automotive/",
        "industries/motorsport/",
        "industries/automotive-research-and-development/",
        "industries/automotive-supply-chain/",
        "industries/energy/",
        "industries/offshore-wind-energy/",
        "industries/oil-and-gas/",
        "industries/electrical-networks/",
        "industries/nuclear-energy/",
        "industries/energy-waste/",
        "industries/advanced-manufacturing/",
    ],
)
def test_cms_918_industries_non_existing_on_international_site(
    endpoint, basic_auth
):
    test_cms_918_redirect_to_international_if_matching_industry_exists(
        endpoint, basic_auth
    )
