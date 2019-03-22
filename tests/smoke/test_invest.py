import pytest
from rest_framework.status import *

from tests import get_absolute_url, join_ui_international, join_ui_invest
from tests.smoke.cms_api_helpers import get_and_assert


@pytest.mark.parametrize(
    "url",
    [
        get_absolute_url("ui-invest:landing"),
        get_absolute_url("ui-invest:contact"),
        get_absolute_url("ui-invest:industries"),
        get_absolute_url("ui-invest:uk-setup-guide"),
        get_absolute_url("ui-invest:hpo-rail"),
        get_absolute_url("ui-invest:hpo-rail-contact"),
        get_absolute_url("ui-invest:hpo-food"),
        get_absolute_url("ui-invest:hpo-food-contact"),
        get_absolute_url("ui-invest:hpo-lightweight"),
        get_absolute_url("ui-invest:hpo-lightweight-contact"),
        get_absolute_url("ui-invest:industries-advanced-manufacturing"),
        get_absolute_url("ui-invest:industries-agri-tech"),
        get_absolute_url("ui-invest:industries-asset-management"),
        get_absolute_url("ui-invest:industries-automotive"),
        get_absolute_url(
            "ui-invest:industries-automotive-research-and-development"
        ),
        get_absolute_url("ui-invest:industries-automotive-supply-chain"),
        get_absolute_url("ui-invest:industries-capital-investment"),
        get_absolute_url("ui-invest:industries-chemicals"),
        get_absolute_url(
            "ui-invest:industries-creative-content-and-production"
        ),
        get_absolute_url("ui-invest:industries-creative-industries"),
        get_absolute_url("ui-invest:industries-data-analytics"),
        get_absolute_url("ui-invest:industries-digital-media"),
        get_absolute_url("ui-invest:industries-electrical-networks"),
        get_absolute_url("ui-invest:industries-energy"),
        get_absolute_url("ui-invest:industries-energy-waste"),
        get_absolute_url("ui-invest:industries-financial-technology"),
        get_absolute_url("ui-invest:industries-food-and-drink"),
        get_absolute_url("ui-invest:industries-food-service-and-catering"),
        get_absolute_url("ui-invest:industries-free-foods"),
        get_absolute_url("ui-invest:industries-meat-poultry-and-dairy"),
        get_absolute_url("ui-invest:industries-medical-technology"),
        get_absolute_url("ui-invest:industries-motorsport"),
        get_absolute_url("ui-invest:industries-nuclear-energy"),
        get_absolute_url("ui-invest:industries-offshore-wind-energy"),
        get_absolute_url("ui-invest:industries-oil-and-gas"),
        get_absolute_url("ui-invest:industries-pharmaceutical-manufacturing"),
        get_absolute_url("ui-invest:industries-retail"),
        get_absolute_url("ui-invest:industries-technology"),
    ],
)
def test_invest_pages(url, basic_auth):
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)


@pytest.mark.stage
@pytest.mark.parametrize(
    "endpoint",
    [
        "industries/health-and-life-sciences/",
        "industries/financial-services/",
        "industries/aerospace/",
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
