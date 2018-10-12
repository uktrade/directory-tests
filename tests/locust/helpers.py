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


class AuthedClientMixin(object):
    def __init__(self):
        super(AuthedClientMixin, self).__init__()
        self.client = AuthenticatedClient(base_url=self.host)


class CMSAPIAuthenticatedClient(DirectoryCMSClient):

    name = None

    def get(self, *args, **kwargs):
        self.name = kwargs.pop("name", None) or self.name
        start_time = time.time()
        status_code = None
        try:
            r = super().get(*args, **kwargs)
            response_time = int(r.raw_response.elapsed.total_seconds() * 1000)
            events.request_success.fire(
                request_type="GET", name=self.name, response_time=response_time,
                response_length=len(r.content))
            status_code = r.status_code
            assert r.status_code in [200, 404]
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
