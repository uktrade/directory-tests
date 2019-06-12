import pytest
from rest_framework.status import *

from tests import join_ui_international, join_ui_invest, URLs
from tests.smoke.cms_api_helpers import get_and_assert


@pytest.mark.parametrize(
    "url",
    [
        URLs.INVEST_LANDING.absolute,
        URLs.INVEST_CONTACT.absolute,
        URLs.INVEST_INDUSTRIES.absolute,
        URLs.INVEST_UK_SETUP_GUIDE.absolute,
        URLs.INVEST_HPO_FOOD.absolute,
        URLs.INVEST_HPO_FOOD_CONTACT.absolute,
        URLs.INVEST_HPO_LIGHTWEIGHT.absolute,
        URLs.INVEST_HPO_LIGHTWEIGHT_CONTACT.absolute,
        URLs.INVEST_HPO_RAIL.absolute,
        URLs.INVEST_HPO_RAIL_CONTACT.absolute,
        URLs.INVEST_INDUSTRIES_AEROSPACE.absolute,
        URLs.INVEST_INDUSTRIES_ADVANCED_MANUFACTURING.absolute,
        URLs.INVEST_INDUSTRIES_AGRI_TECH.absolute,
        URLs.INVEST_INDUSTRIES_ASSET_MANAGEMENT.absolute,
        URLs.INVEST_INDUSTRIES_AUTOMOTIVE.absolute,
        URLs.INVEST_INDUSTRIES_AUTOMOTIVE_RESEARCH_AND_DEVELOPMENT.absolute,
        URLs.INVEST_INDUSTRIES_AUTOMOTIVE_SUPPLY_CHAIN.absolute,
        URLs.INVEST_INDUSTRIES_CAPITAL_INVESTMENT.absolute,
        URLs.INVEST_INDUSTRIES_CHEMICALS.absolute,
        URLs.INVEST_INDUSTRIES_CREATIVE_CONTENT_AND_PRODUCTION.absolute,
        URLs.INVEST_INDUSTRIES_CREATIVE_INDUSTRIES.absolute,
        URLs.INVEST_INDUSTRIES_DATA_ANALYTICS.absolute,
        URLs.INVEST_INDUSTRIES_DIGITAL_MEDIA.absolute,
        URLs.INVEST_INDUSTRIES_ELECTRICAL_NETWORKS.absolute,
        URLs.INVEST_INDUSTRIES_ENERGY.absolute,
        URLs.INVEST_INDUSTRIES_ENERGY_WASTE.absolute,
        URLs.INVEST_INDUSTRIES_FINANCIAL_TECHNOLOGY.absolute,
        URLs.INVEST_INDUSTRIES_FOOD_AND_DRINK.absolute,
        URLs.INVEST_INDUSTRIES_FOOD_SERVICE_AND_CATERING.absolute,
        URLs.INVEST_INDUSTRIES_FREE_FOODS.absolute,
        URLs.INVEST_INDUSTRIES_HEALTH_AND_LIFE_SCIENCES.absolute,
        URLs.INVEST_INDUSTRIES_MEAT_POULTRY_AND_DAIRY.absolute,
        URLs.INVEST_INDUSTRIES_MEDICAL_TECHNOLOGY.absolute,
        URLs.INVEST_INDUSTRIES_MOTORSPORT.absolute,
        URLs.INVEST_INDUSTRIES_NUCLEAR_ENERGY.absolute,
        URLs.INVEST_INDUSTRIES_OFFSHORE_WIND_ENERGY.absolute,
        URLs.INVEST_INDUSTRIES_OIL_AND_GAS.absolute,
        URLs.INVEST_INDUSTRIES_PHARMACEUTICAL_MANUFACTURING.absolute,
        URLs.INVEST_INDUSTRIES_RETAIL.absolute,
        URLs.INVEST_INDUSTRIES_TECHNOLOGY.absolute,
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
    old_url = join_ui_invest(endpoint)
    new_url = join_ui_international(endpoint)
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
