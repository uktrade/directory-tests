import http.client

import requests

from tests import get_absolute_url


def test_terms_200(basic_auth, hawk_cookie):
    response = requests.get(
        get_absolute_url("ui-exred:terms"), auth=basic_auth, cookies=hawk_cookie
    )
    assert response.status_code == http.client.OK


def test_privacy_200(basic_auth, hawk_cookie):
    response = requests.get(
        get_absolute_url("ui-exred:privacy"), auth=basic_auth, cookies=hawk_cookie
    )
    assert response.status_code == http.client.OK


