import pytest
import requests

from tests import get_absolute_url, users


@pytest.fixture
def logged_in_session():
    session = requests.Session()
    user = users['verified']
    response = session.post(
        url=get_absolute_url('sso:login'),
        data={'login': user['username'], 'password': user['password']}
    )
    assert 'Logout' in response.content
    return session
