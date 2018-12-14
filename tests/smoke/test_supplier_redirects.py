import pytest
import requests

from tests import join_ui_supplier


@pytest.mark.dev
@pytest.mark.parametrize("new_url,old_url", [
    ('/industries/healthcare/', join_ui_supplier('industries/health/')),
    ('/industries/technology/', join_ui_supplier('industries/tech/')),
    ('/industries/creative-services/', join_ui_supplier('industries/creative/')),
])
def test_ed_4152_redirect_on_dev_from_old_industry_page(
        new_url, old_url, hawk_cookie):
    response = requests.get(
        old_url, allow_redirects=False, cookies=hawk_cookie
    )

    error_msg = (f"Expected request to '{old_url}' to be redirected to "
                 f"'{new_url}' but instead it was redirected to "
                 f"'{response.headers['Location']}'")
    assert response.headers['Location'] == new_url, error_msg


@pytest.mark.stage
@pytest.mark.parametrize("new_url,old_url", [
    ('/trade/industries/healthcare/', join_ui_supplier('industries/health/')),
    ('/trade/industries/technology/', join_ui_supplier('industries/tech/')),
    ('/trade/industries/creative-services/', join_ui_supplier('industries/creative/')),
])
def test_ed_4152_redirect_on_stage_from_old_industry_page(
        new_url, old_url, hawk_cookie):
    response = requests.get(
        old_url, allow_redirects=False, cookies=hawk_cookie
    )

    error_msg = (f"Expected request to '{old_url}' to be redirected to "
                 f"'{new_url}' but instead it was redirected to "
                 f"'{response.headers['Location']}'")
    assert response.headers['Location'] == new_url, error_msg
