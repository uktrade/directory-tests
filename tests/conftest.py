import pytest
import requests
from directory_api_client.testapiclient import DirectoryTestAPIClient

from tests import get_absolute_url, users
from tests.settings import CMS_SIGNATURE_SECRET_API_KEY


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


@pytest.fixture
def cms_client():
    base_url = get_absolute_url('cms-healthcheck:landing')
    return DirectoryTestAPIClient(
        base_url=base_url, api_key=CMS_SIGNATURE_SECRET_API_KEY)
