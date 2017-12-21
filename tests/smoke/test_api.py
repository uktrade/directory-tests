import http.client

import requests

from tests import get_absolute_url
from tests.settings import DIRECTORY_API_HEALTH_CHECK_TOKEN as TOKEN


def test_api_database_health_check():
    params = {'token': TOKEN}
    response = requests.get(
            get_absolute_url('api:healthcheck-database'), params=params)
    assert response.status_code == http.client.OK


def test_api_cache_health_check():
    params = {'token': TOKEN}
    response = requests.get(
            get_absolute_url('api:healthcheck-cache'), params=params)
    assert response.status_code == http.client.OK


def test_api_elasticsearch_health_check():
    params = {'token': TOKEN}
    response = requests.get(
            get_absolute_url('api:healthcheck-elasticsearch'), params=params)
    assert response.status_code == http.client.OK


def test_ui_buyer_api_health_check():
    params = {'token': TOKEN}
    response = requests.get(
            get_absolute_url('ui-buyer:healthcheck-api'), params=params)
    assert response.status_code == http.client.OK


def test_sso_database_health_check():
    params = {'token': TOKEN}
    response = requests.get(
            get_absolute_url('sso:healthcheck-database'), params=params)
    assert response.status_code == http.client.OK
