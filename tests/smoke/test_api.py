import httplib

import requests

from tests import get_absolute_url


def test_api_connection():
    response = requests.get(get_absolute_url('api:docs'))
    assert response.status_code == httplib.FORBIDDEN
