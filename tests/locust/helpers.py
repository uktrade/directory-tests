import random
import time
from hashlib import sha256
from http import cookies
from urllib.parse import urlsplit

from bs4 import BeautifulSoup
from locust import HttpLocust, events
from locust.clients import LocustResponse, HttpSession
from requests import Request, Session
from requests.exceptions import (
    RequestException,
    MissingSchema,
    InvalidSchema,
    InvalidURL
)

from tests import get_relative_url, settings
from tests.settings import (
    DIRECTORY_API_URL,
    DIRECTORY_API_CLIENT_KEY,
    DIRECTORY_CMS_API_CLIENT_API_KEY,
    DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT,
    DIRECTORY_CMS_API_CLIENT_SENDER_ID,
)
from django.conf import settings as django_settings
django_settings.configure(
    DIRECTORY_API_CLIENT_BASE_URL=DIRECTORY_API_URL,
    DIRECTORY_API_CLIENT_API_KEY=DIRECTORY_API_CLIENT_KEY,
    DIRECTORY_API_CLIENT_SENDER_ID="directory",
    DIRECTORY_API_CLIENT_DEFAULT_TIMEOUT=30,
    DIRECTORY_SSO_API_CLIENT_BASE_URL=None,
    DIRECTORY_SSO_API_CLIENT_API_KEY=None,
    DIRECTORY_SSO_API_CLIENT_SENDER_ID=None,
    DIRECTORY_SSO_API_CLIENT_DEFAULT_TIMEOUT=None,
    DIRECTORY_CMS_API_CLIENT_BASE_URL=None,
    DIRECTORY_CMS_API_CLIENT_API_KEY=None,
    DIRECTORY_CMS_API_CLIENT_SENDER_ID=None,
    DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT=None,
    DIRECTORY_CMS_API_CLIENT_SERVICE_NAME=None,
    CACHES={
        'cms_fallback': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }
)
# this has to be imported after django settings are set
from directory_constants.constants import cms as SERVICE_NAMES
from directory_api_client.client import DirectoryAPIClient
from directory_cms_client.client import DirectoryCMSClient

from tests.locust import USER_CREDENTIALS


class AuthenticatedClient(HttpSession):
    def _send_request_safe_mode(self, method, url, **kwargs):
        kwargs.pop('allow_redirects', None)
        try:
            request = Request(method=method, url=url, **kwargs)
            signed_request = self.sign_request(
                api_key=DIRECTORY_API_CLIENT_KEY,
                prepared_request=request.prepare(),
            )
            return Session().send(signed_request)
        except (MissingSchema, InvalidSchema, InvalidURL):
            raise
        except RequestException as e:
            r = LocustResponse()
            r.error = e
            r.status_code = 0  # with this status_code, content returns None
            r.request = Request(method, url).prepare()
            return r

    def sign_request(self, api_key, prepared_request):
        url = urlsplit(prepared_request.path_url)
        path = bytes(url.path, 'utf8')
        if url.query:
            path += bytes("?{}".format(url.query), 'utf8')

        salt = bytes(api_key, 'utf8')
        body = prepared_request.body or b""

        if isinstance(body, str):
            body = bytes(body, 'utf8')

        signature = sha256(path + body + salt).hexdigest()
        prepared_request.headers["X-Signature"] = signature

        return prepared_request


class APIAuthedClientForLocust(DirectoryAPIClient):

    name = None
    expected_codes = [200]

    def get(self, *args, **kwargs):
        self.name = kwargs.pop("name", None) or self.name
        self.expected_codes = kwargs.pop("expected_codes", None) or self.expected_codes
        start_time = time.time()
        status_code = None
        response = None
        try:
            response = super().get(*args, **kwargs)
            response_time = int(response.elapsed.total_seconds() * 1000)
            events.request_success.fire(
                request_type="GET", name=self.name, response_time=response_time,
                response_length=len(response.content))
            status_code = response.status_code
            assert status_code in self.expected_codes
        except (MissingSchema, InvalidSchema, InvalidURL):
            raise
        except (AssertionError, RequestException):
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type="GET", name=self.name, response_time=total_time,
                exception=status_code or RequestException.errno)
        return response

    def post(self, *args, **kwargs):
        self.name = kwargs.pop("name", None) or self.name
        self.expected_codes = kwargs.pop("expected_codes", None) or self.expected_codes
        start_time = time.time()
        status_code = None
        response = None
        try:
            response = super().post(*args, **kwargs)
            response_time = int(response.elapsed.total_seconds() * 1000)
            status_code = response.status_code
            assert status_code in self.expected_codes
            events.request_success.fire(
                request_type="POST", name=self.name, response_time=response_time,
                response_length=len(response.content))
        except (MissingSchema, InvalidSchema, InvalidURL):
            raise
        except (AssertionError, RequestException):
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type="POST", name=self.name, response_time=total_time,
                exception=status_code or RequestException.errno)
        return response

    def delete(self, *args, **kwargs):
        self.name = kwargs.pop("name", None) or self.name
        self.expected_codes = kwargs.pop("expected_codes", None) or self.expected_codes
        start_time = time.time()
        status_code = None
        response = None
        try:
            response = super().delete(*args, **kwargs)
            response_time = int(response.elapsed.total_seconds() * 1000)
            status_code = response.status_code
            assert status_code in self.expected_codes
            events.request_success.fire(
                request_type="DELETE", name=self.name, response_time=response_time,
                response_length=len(response.content))
        except (MissingSchema, InvalidSchema, InvalidURL):
            raise
        except (AssertionError, RequestException):
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type="DELETE", name=self.name, response_time=total_time,
                exception=status_code or RequestException.errno)
        return response

    def patch(self, *args, **kwargs):
        self.name = kwargs.pop("name", None) or self.name
        self.expected_codes = kwargs.pop("expected_codes", None) or self.expected_codes
        start_time = time.time()
        status_code = None
        response = None
        try:
            response = super().patch(*args, **kwargs)
            response_time = int(response.elapsed.total_seconds() * 1000)
            status_code = response.status_code
            assert status_code in self.expected_codes
            events.request_success.fire(
                request_type="PATCH", name=self.name, response_time=response_time,
                response_length=len(response.content))
        except (MissingSchema, InvalidSchema, InvalidURL):
            raise
        except (AssertionError, RequestException):
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type="PATCH", name=self.name, response_time=total_time,
                exception=status_code or RequestException.errno)
        return response

    def put(self, *args, **kwargs):
        self.name = kwargs.pop("name", None) or self.name
        self.expected_codes = kwargs.pop("expected_codes", None) or self.expected_codes
        start_time = time.time()
        status_code = None
        response = None
        try:
            response = super().put(*args, **kwargs)
            response_time = int(response.elapsed.total_seconds() * 1000)
            status_code = response.status_code
            assert status_code in self.expected_codes
            events.request_success.fire(
                request_type="PUT", name=self.name, response_time=response_time,
                response_length=len(response.content))
        except (MissingSchema, InvalidSchema, InvalidURL):
            raise
        except (AssertionError, RequestException):
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type="PUT", name=self.name, response_time=total_time,
                exception=status_code or RequestException.errno)
        return response


class AuthedClientMixin(object):
    def __init__(self):
        super(AuthedClientMixin, self).__init__()
        self.client = APIAuthedClientForLocust(
            base_url=self.host,
            api_key=DIRECTORY_API_CLIENT_KEY,
            sender_id="directory",
            timeout=30,
        )


class CMSAPIAuthenticatedClient(DirectoryCMSClient):

    name = None
    expected_codes = [200]

    def get(self, *args, **kwargs):
        self.name = kwargs.pop("name", None) or self.name
        self.expected_codes = kwargs.pop("expected_codes", None) or self.expected_codes
        start_time = time.time()
        status_code = None
        try:
            r = super().get(*args, **kwargs)
            response_time = int(r.raw_response.elapsed.total_seconds() * 1000)
            events.request_success.fire(
                request_type="GET", name=self.name, response_time=response_time,
                response_length=len(r.content))
            status_code = r.status_code
            assert status_code in self.expected_codes
            return r
        except (MissingSchema, InvalidSchema, InvalidURL):
            raise
        except (AssertionError, RequestException) as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type="GET", name=self.name, response_time=total_time,
                exception=status_code or RequestException.errno)

    def lookup_by_slug(self, slug, **kwargs):
        self.name = kwargs.pop("name")
        return super().lookup_by_slug(slug, **kwargs)


class CMSAPIAuthClientMixin(HttpLocust):
    def __init__(self):
        super(CMSAPIAuthClientMixin, self).__init__()
        self.service_name = SERVICE_NAMES.INVEST
        self.client = CMSAPIAuthenticatedClient(
            base_url=self.host,
            api_key=DIRECTORY_CMS_API_CLIENT_API_KEY,
            sender_id=DIRECTORY_CMS_API_CLIENT_SENDER_ID,
            timeout=DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT,
            service_name=SERVICE_NAMES.INVEST,
        )


def extract_main_error(content: str) -> str:
    """Extract error from page's `main` section.

    :param content: a raw HTML content
    :return: error message or empty string if no error is detected
    """
    error_indicators = [
        "error", "errors", "problem", "problems", "fail", "failed", "failure",
        "required", "missing",
    ]
    soup = BeautifulSoup(content, "lxml")
    sections = soup.find_all("main")
    lines = [
        line.strip()
        for section in sections
        for line in section.text.splitlines()
        if line
    ]
    has_errors = any(
        indicator in line.lower()
        for line in lines
        for indicator in error_indicators
    )
    return "\n".join(lines) if has_errors else ""


def get_valid_sso_session_id(*, email: str = None, password: str = None):
    login_url = get_relative_url('sso:login')
    client = HttpSession(settings.DIRECTORY_SSO_URL)

    if not email and not password:
        _, email, password = random.choice(USER_CREDENTIALS)
    data = {"login": email, "password": password}
    with client.get(login_url) as response:
        soup = BeautifulSoup(response.content, 'html.parser')
        csrf_token = soup.find(
            'input', {'name': 'csrfmiddlewaretoken'}
        ).get('value')
    data["csrfmiddlewaretoken"] = csrf_token

    with client.post(login_url, data=data) as response:
        set_cookie = response.history[0].headers['Set-Cookie']
        first_response_cookie = cookies.SimpleCookie()
        first_response_cookie.load(set_cookie)
        last_response_set_cookie = response.headers['Set-Cookie']
        last_response_cookie = cookies.SimpleCookie()
        last_response_cookie.load(last_response_set_cookie)

        first_session = first_response_cookie.get('directory_sso_dev_session')
        second_session = last_response_cookie.get('directory_sso_dev_session')

        session = first_session or second_session

    return session.value


def get_two_valid_sso_sessions():
    _, email_1, password_1 = random.choice(USER_CREDENTIALS)
    _, email_2, password_2 = random.choice(USER_CREDENTIALS)
    while email_1 == email_2:
        _, email_2, password_2 = random.choice(USER_CREDENTIALS)
    session_1 = get_valid_sso_session_id(email=email_1, password=password_1)
    session_2 = get_valid_sso_session_id(email=email_2, password=password_2)
    return session_1, session_2


def authenticate_with_sso():
    login_url = get_relative_url('sso:login')
    client = HttpSession(settings.DIRECTORY_SSO_URL)

    _, email, password = random.choice(USER_CREDENTIALS)
    data = {"login": email, "password": password}
    with client.get(login_url) as response:
        soup = BeautifulSoup(response.content, 'html.parser')
        csrf_token = soup.find(
            'input', {'name': 'csrfmiddlewaretoken'}
        ).get('value')
    data["csrfmiddlewaretoken"] = csrf_token

    with client.post(login_url, data=data) as response:
        set_cookie_header = response.headers['Set-Cookie']
    return set_cookie_header
