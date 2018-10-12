import pytest
import requests

from tests import join_ui_supplier


@pytest.mark.parametrize("new_url,old_url", [
    ('/industries/healthcare/',
     join_ui_supplier('/industries/health/')),
    ('/industries/technology/',
     join_ui_supplier('/industries/tech/')),
    ('/industries/creative-services/',
     join_ui_supplier('/industries/creative/')),
])
def test_ed_4152_redirect_from_old_industry_page(new_url, old_url):
    response = requests.get(old_url, allow_redirects=False)

    error_msg = (f"Expected request to '{old_url}' to be redirected to "
                 f"'{new_url}' but instead it was redirected to "
                 f"'{response.headers['Location']}'")
    assert response.headers['Location'] == new_url, error_msg
