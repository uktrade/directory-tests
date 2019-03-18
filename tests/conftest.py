import pytest
import requests

from directory_constants.constants import cms as SERVICE_NAMES
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
            "cms_fallback": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
                "LOCATION": "unique-snowflake",
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
def basic_auth():
    return HTTPBasicAuth(BASICAUTH_USER, BASICAUTH_PASS)


def extract_csrf_middleware_token(content: str) -> str:
    line = [l for l in content.splitlines() if "csrfmiddlewaretoken" in l][0]
    fields = line.strip().split("'")
    token_position = 5
    return fields[token_position]


@pytest.fixture
@retry(wait_fixed=5000, stop_max_attempt_number=2)
def logged_in_session():
    session = requests.Session()
    login_url = get_absolute_url("sso:login")
    response = session.get(url=login_url, auth=(BASICAUTH_USER, BASICAUTH_PASS))
    assert response.status_code == 200, f"Expected 200 but got {response.status_code} from {response.url}"
    csrfmiddlewaretoken = extract_csrf_middleware_token(response.content.decode("UTF-8"))
    user = users["verified"]
    data = {
        "login": user["username"],
        "password": user["password"],
        "csrfmiddlewaretoken": csrfmiddlewaretoken
    }
    response = session.post(
        url=login_url,
        data=data,
        allow_redirects=True,
        auth=(BASICAUTH_USER, BASICAUTH_PASS),
    )
    assert response.status_code == 200, f"Expected 200 but got {response.status_code} from {response.url}"
    assert "Sign out" in response.content.decode("UTF-8"),  f"Couldn't find 'Sign out' in the response from: {response.url}"
    return session

