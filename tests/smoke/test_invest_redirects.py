import pytest
import requests
from rest_framework.status import *

from tests import join_ui_international
from tests.smoke.cms_api_helpers import status_error


@pytest.mark.skip(reason="see CMS-918 International Industry pages aren't present yet")
@pytest.mark.parametrize("old_url,new_url", [
    ("industries/health-and-life-sciences/", join_ui_international("industries/health-and-life-sciences/")),
    ("industries/pharmaceutical-manufacturing/", join_ui_international("industries/pharmaceutical-manufacturing/")),
    ("industries/medical-technology/", join_ui_international("industries/medical-technology/")),
    ("industries/creative-industries/", join_ui_international("industries/creative-industries/")),
    ("industries/digital-media/", join_ui_international("industries/digital-media/")),
    ("industries/creative-content-and-production/", join_ui_international("industries/creative-content-and-production/")),
    ("industries/food-and-drink/", join_ui_international("industries/food-and-drink/")),
    ("industries/meat-poultry-and-dairy/", join_ui_international("industries/meat-poultry-and-dairy/")),
    ("industries/food-service-and-catering/", join_ui_international("industries/food-service-and-catering/")),
    ("industries/free-foods/", join_ui_international("industries/free-foods/")),
    ("industries/financial-services/", join_ui_international("industries/financial-services/")),
    ("industries/asset-management/", join_ui_international("industries/asset-management/")),
    ("industries/financial-technology/", join_ui_international("industries/financial-technology/")),
    ("industries/aerospace/", join_ui_international("industries/aerospace/")),
    ("industries/agri-tech/", join_ui_international("industries/agri-tech/")),
    ("industries/retail/", join_ui_international("industries/retail/")),
    ("industries/chemicals/", join_ui_international("industries/chemicals/")),
    ("industries/technology/", join_ui_international("industries/technology/")),
    ("industries/data-analytics/", join_ui_international("industries/data-analytics/")),
    ("industries/capital-investment/", join_ui_international("industries/capital-investment/")),
    ("industries/automotive/", join_ui_international("industries/automotive/")),
    ("industries/motorsport/", join_ui_international("industries/motorsport/")),
    ("industries/automotive-research-and-development/", join_ui_international("industries/automotive-research-and-development/")),
    ("industries/automotive-supply-chain/", join_ui_international("industries/automotive-supply-chain/")),
    ("industries/energy/", join_ui_international("industries/energy/")),
    ("industries/offshore-wind-energy/", join_ui_international("industries/offshore-wind-energy/")),
    ("industries/oil-and-gas/", join_ui_international("industries/oil-and-gas/")),
    ("industries/electrical-networks/", join_ui_international("industries/electrical-networks/")),
    ("industries/nuclear-energy/", join_ui_international("industries/nuclear-energy/")),
    ("industries/energy-waste/", join_ui_international("industries/energy-waste/")),
    ("industries/advanced-manufacturing/", join_ui_international("industries/advanced-manufacturing/")),
])
def test_cms_918_redirect_to_international_if_matching_industry_exists(
         old_url, new_url,basic_auth, hawk_cookie):
    """
    A redirect to the International site will happen only if there’s a sector
    page with the same slug in International.
    """
    response = requests.get(
        old_url, allow_redirects=False, auth=basic_auth, cookies=hawk_cookie
    )
    assert response.status_code == HTTP_302_FOUND, status_error(
        HTTP_302_FOUND, response
    )

    error_msg = (f"Expected request to '{old_url}' to be redirected to "
                 f"'{new_url}' but instead it was redirected to "
                 f"'{response.headers['Location']}'")
    assert response.headers["Location"] == new_url, error_msg
