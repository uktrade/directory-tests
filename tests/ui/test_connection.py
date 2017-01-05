import requests

from tests.settings import DIRECTORY_BUYER_UI_URL


def test_ui_connection():
    response = requests.get(DIRECTORY_BUYER_UI_URL)
    assert response.ok
