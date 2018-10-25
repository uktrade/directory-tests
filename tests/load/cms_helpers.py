import time

from locust import HttpLocust, events
from requests.exceptions import (
    InvalidSchema,
    InvalidURL,
    MissingSchema,
    RequestException
)

from tests.settings import (
    DIRECTORY_CMS_API_CLIENT_API_KEY,
    DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT,
    DIRECTORY_CMS_API_CLIENT_SENDER_ID
)
# Initialise CMS Client with dummy ENV Vars as we're going to use a patched
# CMS Client
from django.conf import settings as django_settings
django_settings.configure(
    DIRECTORY_CMS_API_CLIENT_BASE_URL=None,
    DIRECTORY_CMS_API_CLIENT_API_KEY=None,
    DIRECTORY_CMS_API_CLIENT_SENDER_ID=None,
    DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT=None,
    DIRECTORY_CMS_API_CLIENT_SERVICE_NAME=None,
    DIRECTORY_CMS_API_CLIENT_CACHE_EXPIRE_SECONDS=None,
    CACHES={
        "cms_fallback": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake",
        }
    },
)
# these module have to be imported after django settings are set
# otherwise you won't be able to get an instance of CMS Client
from directory_cms_client.client import DirectoryCMSClient
from directory_constants.constants import cms as SERVICE_NAMES


def build_params(
    full_path=None, language_code=None, draft_token=None, fields=None
):
    params = {"fields": fields or ["*"]}
    if language_code:
        params["lang"] = language_code
    if draft_token:
        params["draft_token"] = draft_token
    if full_path:
        params["full_path"] = full_path
    return params


class LocustCMSAPIAuthenticatedClient(DirectoryCMSClient):
    """A CMS API Authenticated Client compatible with Locust Http Client.

    This overwrites `get()` method in order to fire events on success & failure
    and forces helper methods like, `lookup_by_slug()` to use modified `get()`.
    Modified client allows to define a list of expected status codes.
    Comes in handy when expecting ie. 404.
    """

    name = None
    expected_codes = [200]

    def get(self, *args, **kwargs):
        self.name = kwargs.pop("name", None) or self.name
        self.expected_codes = (
            kwargs.pop("expected_codes", None) or self.expected_codes
        )
        start_time = time.time()
        status_code = None
        try:
            r = super().get(*args, **kwargs)
            assert r.raw_response
            response_time = int(r.raw_response.elapsed.total_seconds() * 1000)
            events.request_success.fire(
                request_type="GET",
                name=self.name,
                response_time=response_time,
                response_length=len(r.content),
            )
            status_code = r.status_code
            assert status_code in self.expected_codes
            return r
        except (MissingSchema, InvalidSchema, InvalidURL):
            raise
        except (AssertionError, RequestException):
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type="GET",
                name=self.name,
                response_time=total_time,
                exception=status_code or RequestException.errno,
            )

    def lookup_by_full_path(
        self,
        full_path,
        fields=None,
        draft_token=None,
        language_code=None,
        **kwargs,
    ):
        base_params = build_params(
            fields=fields, language_code=language_code,
            draft_token=draft_token, full_path=full_path
        )
        return self.get(
            url=self.endpoints["page-by-full-path"],
            params={**base_params},
            **kwargs,
        )

    def lookup_by_slug(
        self, slug, fields=None, draft_token=None, language_code=None, **kwargs
    ):
        base_params = build_params(
            fields=fields, language_code=language_code, draft_token=draft_token
        )
        return self.get(
            url=self.endpoints["page-by-slug"].format(slug=slug),
            params={**base_params},
            **kwargs,
        )


class CMSAPIAuthClientMixin(HttpLocust):
    def __init__(self):
        super(CMSAPIAuthClientMixin, self).__init__()
        self.client = LocustCMSAPIAuthenticatedClient(
            base_url=self.host,
            api_key=DIRECTORY_CMS_API_CLIENT_API_KEY,
            sender_id=DIRECTORY_CMS_API_CLIENT_SENDER_ID,
            timeout=DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT,
            default_service_name=SERVICE_NAMES.INVEST,
        )
