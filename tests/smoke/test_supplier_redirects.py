import pytest
import requests

from tests import join_ui_supplier, get_absolute_url


@pytest.mark.parametrize("new_url,old_url", [
    (get_absolute_url('ui-supplier:industries-health'),
     join_ui_supplier('/industries/health/')),
    (get_absolute_url('ui-supplier:industries-tech'),
     join_ui_supplier('/industries/tech/')),
    (get_absolute_url('ui-supplier:industries-creative'),
     join_ui_supplier('/industries/creative/')),
])
def test_ed_4152_redirect_from_old_industry_page(new_url, old_url):
    response = requests.get(old_url, allow_redirects=False)

    assert response.headers['Location'] == new_url
