import pytest
import requests
from rest_framework.status import *

from tests import join_ui_supplier
from tests.smoke.cms_api_helpers import status_error


@pytest.mark.parametrize("new_url,old_url", [
    ('/trade/industries/healthcare/', join_ui_supplier('industries/health/')),
    ('/trade/industries/technology/', join_ui_supplier('industries/tech/')),
    ('/trade/industries/creative-services/', join_ui_supplier('industries/creative/')),
])
def test_ed_4152_redirect_on_stage_from_old_industry_page(
        new_url, old_url, basic_auth):
    response = requests.get(
        old_url, allow_redirects=False, auth=basic_auth
    )
    assert response.status_code == HTTP_302_FOUND, status_error(
        HTTP_302_FOUND, response
    )

    error_msg = (f"Expected request to '{old_url}' to be redirected to "
                 f"'{new_url}' but instead it was redirected to "
                 f"'{response.headers['Location']}'")
    assert response.headers['Location'] == new_url, error_msg
