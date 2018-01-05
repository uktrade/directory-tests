import http.client

import pytest
import requests

from tests import get_absolute_url
from tests.settings import DIRECTORY_API_HEALTH_CHECK_TOKEN as TOKEN


@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('api:healthcheck-database'),
    get_absolute_url('api:healthcheck-cache'),
    get_absolute_url('api:healthcheck-elasticsearch'),
])
def test_health_check_endpoints(absolute_url):
    params = {'token': TOKEN}
    response = requests.get(absolute_url, params=params)
    assert response.status_code == http.client.OK
