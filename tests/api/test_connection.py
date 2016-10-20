import requests

from tests.settings import DIRECTORY_API_URL


def test_api_connection():
    response = requests.get('{}/docs/'.format(DIRECTORY_API_URL))
    assert response.ok
