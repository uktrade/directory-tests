# -*- coding: utf-8 -*-
import time

from locust import HttpLocust, events
from requests.exceptions import (
    InvalidSchema,
    InvalidURL,
    MissingSchema,
    RequestException,
)

from directory_cms_client.client import DirectoryCMSClient  # noqa
from directory_constants.cms import INVEST  # noqa
from directory_tests_shared.settings import (
    CMS_API_DEFAULT_TIMEOUT,
    CMS_API_KEY,
    CMS_API_SENDER_ID,
)


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
        self.expected_codes = kwargs.pop("expected_codes", None) or self.expected_codes
        start_time = time.time()
        status_code = None
        try:
            r = super().get(*args, **kwargs)
            status_code = r.status_code
            response_time = int((time.time() - start_time) * 1000)
            if hasattr(r, "raw_response"):
                if hasattr(r.raw_response, "elapsed"):
                    response_time = int(r.raw_response.elapsed.total_seconds() * 1000)
            assert status_code in self.expected_codes
            events.request_success.fire(
                request_type="GET",
                name=self.name,
                response_time=response_time,
                response_length=len(r.content),
            )
            return r
        except (MissingSchema, InvalidSchema, InvalidURL):
            raise
        except (AssertionError, RequestException):
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type="GET",
                name=self.name,
                response_time=total_time,
                response_length=0,
                exception=status_code or RequestException.errno,
            )


class CMSAPIAuthClientMixin(HttpLocust):
    def __init__(self):
        super(CMSAPIAuthClientMixin, self).__init__()
        self.client = LocustCMSAPIAuthenticatedClient(
            base_url=self.host,
            api_key=CMS_API_KEY,
            sender_id=CMS_API_SENDER_ID,
            timeout=CMS_API_DEFAULT_TIMEOUT,
            default_service_name=INVEST,
        )
