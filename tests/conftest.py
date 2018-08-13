import pytest
import requests

from tests import get_absolute_url, users
from tests.settings import (
    CMS_SIGNATURE_SECRET_API_KEY,
    SSO_API_SIGNATURE_SECRET,
)


@pytest.fixture
def logged_in_session():
    session = requests.Session()
    user = users['verified']
    response = session.post(
        url=get_absolute_url('sso:login'),
        data={'login': user['username'], 'password': user['password']}
    )
    assert 'Sign out' in str(response.content)
    return session
