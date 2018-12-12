import pytest
import requests

from directory_constants.constants import cms as SERVICE_NAMES
from mohawk import Sender
from retrying import retry

from tests import get_absolute_url, users
from tests.settings import (
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
    IP_RESTRICTOR_SKIP_CHECK_SECRET_CMS,
    IP_RESTRICTOR_SKIP_CHECK_SECRET_EXRED,
    IP_RESTRICTOR_SKIP_CHECK_SECRET_FAB,
    IP_RESTRICTOR_SKIP_CHECK_SECRET_FAS,
    IP_RESTRICTOR_SKIP_CHECK_SECRET_FORMS,
    IP_RESTRICTOR_SKIP_CHECK_SECRET_INVEST,
    IP_RESTRICTOR_SKIP_CHECK_SECRET_SSO,
    IP_RESTRICTOR_SKIP_CHECK_SECRET_SUD,
    DIRECTORY_SSO_URL,
    DIRECTORY_PROFILE_URL,
    DIRECTORY_UI_BUYER_URL,
    DIRECTORY_UI_SUPPLIER_URL,
    EXRED_UI_URL,
    INVEST_UI_URL,
    OLD_DIRECTORY_UI_SUPPLIER_URL,
    OLD_EXRED_UI_URL,
)


def pytest_configure():
    from django.conf import settings
    settings.configure(
        DIRECTORY_SSO_API_CLIENT_BASE_URL=DIRECTORY_SSO_API_CLIENT_BASE_URL,
        DIRECTORY_SSO_API_CLIENT_API_KEY=DIRECTORY_SSO_API_CLIENT_API_KEY,
        DIRECTORY_SSO_API_CLIENT_SENDER_ID=DIRECTORY_SSO_API_CLIENT_SENDER_ID,
        DIRECTORY_SSO_API_CLIENT_DEFAULT_TIMEOUT=DIRECTORY_SSO_API_CLIENT_DEFAULT_TIMEOUT,

        DIRECTORY_CMS_API_CLIENT_CACHE_EXPIRE_SECONDS=DIRECTORY_CMS_API_CLIENT_CACHE_EXPIRE_SECONDS,

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
def cms_client():
    from directory_cms_client.client import DirectoryCMSClient
    return DirectoryCMSClient(
        base_url=DIRECTORY_CMS_API_CLIENT_BASE_URL,
        api_key=DIRECTORY_CMS_API_CLIENT_API_KEY,
        sender_id=DIRECTORY_CMS_API_CLIENT_SENDER_ID,
        timeout=DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT,
        default_service_name="change-me",
    )


def hawk_cookie(key):
    sender = Sender(
        credentials={
            'id': IP_RESTRICTOR_SKIP_CHECK_SENDER_ID,
            'key': key,
            'algorithm': 'sha256'
        },
        url='/',
        method='',
        always_hash_content=False
    )
    return {"ip-restrict-signature": sender.request_header}


@pytest.fixture
def cms_hawk_cookie():
    return hawk_cookie(IP_RESTRICTOR_SKIP_CHECK_SECRET_CMS)


@pytest.fixture
def fab_hawk_cookie():
    return hawk_cookie(IP_RESTRICTOR_SKIP_CHECK_SECRET_FAB)


@pytest.fixture
def fas_hawk_cookie():
    return hawk_cookie(IP_RESTRICTOR_SKIP_CHECK_SECRET_FAS)


@pytest.fixture
def exred_hawk_cookie():
    return hawk_cookie(IP_RESTRICTOR_SKIP_CHECK_SECRET_EXRED)


@pytest.fixture
def invest_hawk_cookie():
    return hawk_cookie(IP_RESTRICTOR_SKIP_CHECK_SECRET_INVEST)


@pytest.fixture
def sso_hawk_cookie():
    return hawk_cookie(IP_RESTRICTOR_SKIP_CHECK_SECRET_SSO)


@pytest.fixture
def sud_hawk_cookie():
    return hawk_cookie(IP_RESTRICTOR_SKIP_CHECK_SECRET_SUD)


@pytest.fixture
@retry(wait_fixed=5000, stop_max_attempt_number=2)
def logged_in_session():
    session = requests.Session()
    user = users['verified']
    response = session.post(
        url=get_absolute_url('sso:login'),
        data={'login': user['username'], 'password': user['password']}
    )
    assert 'Sign out' in str(response.content)
    return session
