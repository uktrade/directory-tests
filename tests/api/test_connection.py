import httplib

import requests
import pytest

from tests import get_absolute_url


@pytest.mark.skip(reason="not working and want to run load tests")
def test_api_connection():
    response = requests.get(get_absolute_url('api:docs'))
    assert response.status_code == httplib.FORBIDDEN
