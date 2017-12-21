import http.client

import requests

from tests import get_absolute_url
from tests.settings import DIRECTORY_API_HEALTH_CHECK_TOKEN as TOKEN


def test_healthcheck_api():
    params = {'token': TOKEN}
    response = requests.get(
            get_absolute_url('ui-exred:healthcheck-api'), params=params)
    assert response.status_code == http.client.OK


def test_healthcheck_sso_proxy():
    params = {'token': TOKEN}
    response = requests.get(
            get_absolute_url('ui-exred:healthcheck-sso-proxy'), params=params)
    assert response.status_code == http.client.OK
