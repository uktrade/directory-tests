import pytest
import requests

from directory_constants.constants import cms as SERVICE_NAMES
from mohawk import Sender
from requests.auth import HTTPBasicAuth
from retrying import retry

from tests import get_absolute_url, users
from tests.settings import (
    BASICAUTH_USER,
    BASICAUTH_PASS,
    DIRECTORY_CMS_API_CLIENT_API_KEY,
    DIRECTORY_CMS_API_CLIENT_BASE_URL,
    DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT,
    DIRECTORY_CMS_API_CLIENT_SENDER_ID,
    DIRECTORY_SSO_API_CLIENT_API_KEY,
    DIRECTORY_SSO_API_CLIENT_BASE_URL,
    DIRECTORY_SSO_API_CLIENT_DEFAULT_TIMEOUT,
    DIRECTORY_SSO_API_CLIENT_SENDER_ID,
    DIRECTORY_CMS_API_CLIENT_CACHE_EXPIRE_SECONDS,
    IP_RESTRICTOR_SKIP_CHECK_SENDER_ID,
    IP_RESTRICTOR_SKIP_CHECK_SECRET,
)


def pytest_configure():
    from django.conf import settings
    settings.configure(
        DIRECTORY_CLIENT_CORE_CACHE_EXPIRE_SECONDS=30,

        DIRECTORY_SSO_API_CLIENT_BASE_URL=DIRECTORY_SSO_API_CLIENT_BASE_URL,
        DIRECTORY_SSO_API_CLIENT_API_KEY=DIRECTORY_SSO_API_CLIENT_API_KEY,
        DIRECTORY_SSO_API_CLIENT_SENDER_ID=DIRECTORY_SSO_API_CLIENT_SENDER_ID,
        DIRECTORY_SSO_API_CLIENT_DEFAULT_TIMEOUT=DIRECTORY_SSO_API_CLIENT_DEFAULT_TIMEOUT,
        DIRECTORY_CMS_API_CLIENT_CACHE_EXPIRE_SECONDS=DIRECTORY_CMS_API_CLIENT_CACHE_EXPIRE_SECONDS,

        DIRECTORY_CMS_API_CLIENT_BASE_URL=DIRECTORY_CMS_API_CLIENT_BASE_URL,
        DIRECTORY_CMS_API_CLIENT_API_KEY=DIRECTORY_CMS_API_CLIENT_API_KEY,
        DIRECTORY_CMS_API_CLIENT_SENDER_ID=DIRECTORY_CMS_API_CLIENT_SENDER_ID,
        DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT=DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT,
        DIRECTORY_CMS_API_CLIENT_SERVICE_NAME=SERVICE_NAMES.EXPORT_READINESS,
        CACHES={
            'cms_fallback': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'unique-snowflake',
            }
        }
    )


@pytest.fixture
def cms_client():
    from directory_cms_client.client import DirectoryCMSClient
    return DirectoryCMSClient(
        base_url=DIRECTORY_CMS_API_CLIENT_BASE_URL,
        api_key=DIRECTORY_CMS_API_CLIENT_API_KEY,
        sender_id=DIRECTORY_CMS_API_CLIENT_SENDER_ID,
        timeout=DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT,
        default_service_name="change-me",
    )


@pytest.fixture
def hawk_cookie():
    sender = Sender(
        credentials={
            'id': IP_RESTRICTOR_SKIP_CHECK_SENDER_ID,
            'key': IP_RESTRICTOR_SKIP_CHECK_SECRET,
            'algorithm': 'sha256'
        },
        url='/',
        method='',
        always_hash_content=False
    )
    return {"ip-restrict-signature": sender.request_header}


@pytest.fixture
@retry(wait_fixed=5000, stop_max_attempt_number=2)
def logged_in_session(hawk_cookie):
    session = requests.Session()
    user = users['verified']
    response = session.post(
        url=get_absolute_url('sso:login'),
        data={'login': user['username'], 'password': user['password']},
        cookies=hawk_cookie,
    )
    assert 'Sign out' in str(response.content)
    return session


@pytest.fixture
def basic_auth():
    return HTTPBasicAuth(BASICAUTH_USER, BASICAUTH_PASS)
