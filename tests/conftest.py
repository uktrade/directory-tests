import pytest
import requests
from tests import get_absolute_url, users
from tests.settings import (
    DIRECTORY_CMS_API_CLIENT_API_KEY,
    DIRECTORY_CMS_API_CLIENT_BASE_URL,
    DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT,
    DIRECTORY_CMS_API_CLIENT_SENDER_ID,
    DIRECTORY_SSO_API_CLIENT_API_KEY,
    DIRECTORY_SSO_API_CLIENT_BASE_URL,
    DIRECTORY_SSO_API_CLIENT_DEFAULT_TIMEOUT,
    DIRECTORY_SSO_API_CLIENT_SENDER_ID
)


def pytest_configure():
    from django.conf import settings
    settings.configure(
        DIRECTORY_SSO_API_CLIENT_BASE_URL=DIRECTORY_SSO_API_CLIENT_BASE_URL,
        DIRECTORY_SSO_API_CLIENT_API_KEY=DIRECTORY_SSO_API_CLIENT_API_KEY,
        DIRECTORY_SSO_API_CLIENT_SENDER_ID=DIRECTORY_SSO_API_CLIENT_SENDER_ID,
        DIRECTORY_SSO_API_CLIENT_DEFAULT_TIMEOUT=DIRECTORY_SSO_API_CLIENT_DEFAULT_TIMEOUT,

        DIRECTORY_CMS_API_CLIENT_BASE_URL=DIRECTORY_CMS_API_CLIENT_BASE_URL,
        DIRECTORY_CMS_API_CLIENT_API_KEY=DIRECTORY_CMS_API_CLIENT_API_KEY,
        DIRECTORY_CMS_API_CLIENT_SENDER_ID=DIRECTORY_CMS_API_CLIENT_SENDER_ID,
        DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT=DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT,
        DIRECTORY_CMS_API_CLIENT_SERVICE_NAME=SERVICE_NAMES.FIND_A_SUPPLIER,
        CACHES={
            'cms_fallback': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'unique-snowflake',
            }
        }
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
