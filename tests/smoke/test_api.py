import http.client

import requests

from tests import get_absolute_url
from tests.settings import DIRECTORY_API_HEALTH_CHECK_TOKEN as TOKEN


def test_healthcheck_database():
    params = {'token': TOKEN}
    response = requests.get(
            get_absolute_url('api:healthcheck-database'), params=params)
    assert response.status_code == http.client.OK


def test_healthcheck_cache():
    params = {'token': TOKEN}
    response = requests.get(
            get_absolute_url('api:healthcheck-cache'), params=params)
    assert response.status_code == http.client.OK


def test_healthcheck_elasticsearch():
    params = {'token': TOKEN}
    response = requests.get(
            get_absolute_url('api:healthcheck-elasticsearch'), params=params)
    assert response.status_code == http.client.OK
