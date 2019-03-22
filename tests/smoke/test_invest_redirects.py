import pytest
from rest_framework.status import *

from tests import join_ui_international, join_ui_invest
from tests.smoke.cms_api_helpers import get_and_assert


@pytest.mark.skip(reason="these International Industry pages aren't present yet")
@pytest.mark.stage
@pytest.mark.parametrize(
    "old_url,new_url",
    [
        ("industries/pharmaceutical-manufacturing/", "industries/pharmaceutical-manufacturing/"),
        ("industries/medical-technology/", "industries/medical-technology/"),
        ("industries/creative-industries/", "industries/creative-industries/"),
        ("industries/digital-media/", "industries/digital-media/"),
        ("industries/creative-content-and-production/", "industries/creative-content-and-production/"),
        ("industries/food-and-drink/", "industries/food-and-drink/"),
        ("industries/meat-poultry-and-dairy/", "industries/meat-poultry-and-dairy/"),
        ("industries/food-service-and-catering/", "industries/food-service-and-catering/"),
        ("industries/free-foods/", "industries/free-foods/"),
        ("industries/asset-management/", "industries/asset-management/"),
        ("industries/financial-technology/", "industries/financial-technology/"),
        ("industries/agri-tech/", "industries/agri-tech/"),
        ("industries/retail/", "industries/retail/"),
        ("industries/chemicals/", "industries/chemicals/"),
        ("industries/technology/", "industries/technology/"),
        ("industries/data-analytics/", "industries/data-analytics/"),
        ("industries/capital-investment/", "industries/capital-investment/"),
        ("industries/automotive/", "industries/automotive/"),
        ("industries/motorsport/", "industries/motorsport/"),
        ("industries/automotive-research-and-development/", "industries/automotive-research-and-development/"),
        ("industries/automotive-supply-chain/", "industries/automotive-supply-chain/"),
        ("industries/energy/", "industries/energy/"),
        ("industries/offshore-wind-energy/", "industries/offshore-wind-energy/"),
        ("industries/oil-and-gas/", "industries/oil-and-gas/"),
        ("industries/electrical-networks/", "industries/electrical-networks/"),
        ("industries/nuclear-energy/", "industries/nuclear-energy/"),
        ("industries/energy-waste/", "industries/energy-waste/"),
        ("industries/advanced-manufacturing/", "industries/advanced-manufacturing/"),
    ],
)
def test_cms_918_redirect_to_international_if_matching_industry_exists(
    old_url, new_url, basic_auth
):
    """
    A redirect to the International site will happen only if there’s a sector
    page with the same slug in International.
    """
    response = get_and_assert(
        url=join_ui_invest(old_url),
        allow_redirects=False,
        status_code=HTTP_302_FOUND,
        auth=basic_auth,
    )

    error_msg = (
        f"Expected request to '{old_url}' to be redirected to "
        f"'{new_url}' but instead it was redirected to "
        f"'{response.headers['Location']}'"
    )
    assert response.headers["Location"] == join_ui_international(new_url), error_msg


@pytest.mark.stage
@pytest.mark.parametrize(
    "old_url,new_url",
    [
        ("industries/health-and-life-sciences/", "industries/health-and-life-sciences/"),
        ("industries/financial-services/", "industries/financial-services/"),
        ("industries/aerospace/", "industries/aerospace/"),
    ],
)
def test_cms_918_redirect_to_international_if_matching_industry_exists_working(
    old_url, new_url, basic_auth
):
    """
    A redirect to the International site will happen only if there’s a sector
    page with the same slug in International.
    """
    response = get_and_assert(
        url=join_ui_invest(old_url),
        allow_redirects=False,
        status_code=HTTP_302_FOUND,
        auth=basic_auth,
    )

    error_msg = (
        f"Expected request to '{old_url}' to be redirected to "
        f"'{new_url}' but instead it was redirected to "
        f"'{response.headers['Location']}'"
    )
    assert response.headers["Location"] == join_ui_international(new_url), error_msg
