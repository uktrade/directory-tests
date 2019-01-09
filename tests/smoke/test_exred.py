import http.client

import requests

from tests import get_absolute_url


def test_terms_200(hawk_cookie):
    response = requests.get(
        get_absolute_url('ui-exred:terms'), cookies=hawk_cookie
    )
    assert response.status_code == http.client.OK


def test_privacy_200(hawk_cookie):
    response = requests.get(
        get_absolute_url('ui-exred:privacy'), cookies=hawk_cookie
    )
    assert response.status_code == http.client.OK


