import requests

from tests.settings import DIRECTORY_UI_BUYER_URL


def test_ui_connection():
    response = requests.get(DIRECTORY_UI_BUYER_URL)
    assert response.ok
