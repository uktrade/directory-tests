# -*- coding: utf-8 -*-
import time

from locust import HttpUser, events
from requests.exceptions import (
    InvalidSchema,
    InvalidURL,
    MissingSchema,
    RequestException,
)

from directory_cms_client.client import DirectoryCMSClient, cms_api_client  # noqa
from directory_constants.cms import INVEST  # noqa
from directory_tests_shared.settings import (
    CMS_API_DEFAULT_TIMEOUT,
    CMS_API_KEY,
    CMS_API_SENDER_ID,
)


def get_page_types():
    response = cms_api_client.get("/api/pages/types/")
    assert response.status_code == 200
    all_page_types = response.json()["types"]
    skipped_page_types = ["wagtailcore.page", "components.bannercomponent"]
    page_types = sorted(list(set(all_page_types) - set(skipped_page_types)))
    return page_types


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
            if hasattr(r, "status_code"):
                print(f"GET {args[0]} -> {r.status_code}")


class CMSAPIAuthClientMixin(HttpUser):
    def __init__(self, *args, **kwargs):
        super(CMSAPIAuthClientMixin, self).__init__(*args, **kwargs)
        self.client = LocustCMSAPIAuthenticatedClient(
            base_url=self.host,
            api_key=CMS_API_KEY,
            sender_id=CMS_API_SENDER_ID,
            timeout=CMS_API_DEFAULT_TIMEOUT,
            default_service_name=INVEST,
        )
