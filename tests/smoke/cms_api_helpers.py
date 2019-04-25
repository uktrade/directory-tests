import asyncio
import logging
from collections import defaultdict
from pprint import pformat
from typing import List, Tuple, Union
from urllib.parse import urlparse

import requests
from directory_client_core.helpers import AbstractResponse
from directory_cms_client import DirectoryCMSClient
from directory_cms_client.client import cms_api_client
from directory_constants.constants import cms as SERVICE_NAMES
from requests import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_302_FOUND,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)
from retrying import retry

from tests import get_absolute_url, get_relative_url
from tests.settings import (
    DIRECTORY_CMS_API_CLIENT_API_KEY,
    DIRECTORY_CMS_API_CLIENT_BASE_URL,
    DIRECTORY_CMS_API_CLIENT_SENDER_ID,
)


class AsyncDirectoryCMSClient(DirectoryCMSClient):
    """Make CMS Client work with AsyncIO"""

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        pass


def async_cms_client():
    return AsyncDirectoryCMSClient(
        base_url=DIRECTORY_CMS_API_CLIENT_BASE_URL,
        api_key=DIRECTORY_CMS_API_CLIENT_API_KEY,
        sender_id=DIRECTORY_CMS_API_CLIENT_SENDER_ID,
        timeout=55,
        default_service_name=SERVICE_NAMES.INVEST,
    )


async def fetch(endpoints: List[str]):
    async_loop = asyncio.get_event_loop()
    async with async_cms_client() as client:
        futures = [
            async_loop.run_in_executor(None, client.get, endpoint)
            for endpoint in endpoints
        ]
        return await asyncio.gather(*futures)


def check_for_special_urls_cases(url: str) -> str:
    # this was added because of BUG CMS-416
    if "setup-guides" in url:
        url = url.replace("setup-guides", "uk-setup-guide")
    if "setup-guide-landing" in url:
        url = url.replace("setup-guide-landing", "uk-setup-guide")
    if "setup-guide-landing-page/" in url:
        url = url.replace("setup-guide-landing-page/", "")
    if "performance-dashboard-" in url:
        url = url.replace("performance-dashboard-", "performance-dashboard/")
    if "high-potential-opportunity-submit-success" in url:
        url = url.replace("high-potential-opportunity-submit-success", "success")
    return url


def check_for_special_page_cases(page: dict) -> str:
    if page["page_type"] in [
        "ArticlePage",
        "ArticleListingPage",
        "SuperregionPage",
        "CountryGuidePage",
    ]:
        url = check_for_special_urls_cases(page["full_url"])
    elif page["page_type"] in ["ContactSuccessPage", "ContactUsGuidancePage"]:
        # contact-us success page URLs are broken
        # we need to remove last part of the URL path
        url = page["meta"]["url"]
        p = urlparse(page["meta"]["url"])
        short_path = p.path[: p.path.rfind("/", 0, p.path.rfind("/", 0)) + 1]
        url = url.replace(p.path, short_path)
    elif page["page_type"] in [
        "InvestHomePage",
        "LandingPage",
        "HomePage",
        "InternationalLandingPage",
    ]:
        # All draft version of pages that use CMS components are affected by bug CMS-754
        # invest homepage
        # fas homepage
        # exred international page
        # exred international
        # domestic eu-exit-news list
        skip_full_paths = [
            "/home-page/",  # Invest home page
            "/landing-page/",  # FAS home page
            "/home/",  # ExRed home page
            "/international/",  # International landing page
        ]
        if any(True for path in skip_full_paths if page["full_path"] == path):
            if page["meta"]["draft_token"]:
                url = "http://skip.this.url/check/CMS-754"
            else:
                url = page["meta"]["url"]
        else:
            url = page["meta"]["url"]
    else:
        url = page["meta"]["url"]
    return url


def should_skip_never_published_page(response: AbstractResponse) -> bool:
    if response.status_code == HTTP_404_NOT_FOUND:
        print(
            f"GET {response.raw_response.request.url} → 404. Maybe this page was never published"
        )
        return True
    return False


def should_skip_url(url: str) -> bool:
    skip = [
        "/markets/",  # ATM there's no landing page for markets
        "/asia-pacific/",  #
        "country-guides",  # Country guides are not ready for testing
        "/international/",  # International news aren't always enabled
        "/eu-exit-news/",  # International news aren't always enabled
        "contact/find-uk-companies/success/",  # this page is not in use anymore
        "skip.this.url",  # skip URL which was deemed to skip the page checker
    ]
    if any(True for bit in skip if bit in url):
        return True

    skip_endings = [
        "uk-regions/",  # this was added because of CMS-413
        "uk-regions",  # there's no landing page for UK Regions
    ]
    if any(True for bit in skip_endings if url.endswith(bit)):
        return True

    return False


def status_error(
    expected_status_code: int, response: Union[AbstractResponse, Response]
):
    if isinstance(response, AbstractResponse):
        return (
            f"{response.raw_response.request.method} {response.raw_response.url} "
            f"returned {response.status_code} instead of expected "
            f"{expected_status_code}\n"
            f"REQ headers: {pformat(response.raw_response.request.headers)}\n"
            f"RSP headers: {pformat(response.raw_response.headers)}"
        )
    elif isinstance(response, Response):
        return (
            f"{response.request.method} {response.url} "
            f"returned {response.status_code} instead of expected "
            f"{expected_status_code}\n"
            f"REQ headers: {pformat(response.request.headers)}\n"
            f"RSP headers: {pformat(response.headers)}"
        )


def get_and_assert(
    url: str,
    status_code: int,
    *,
    auth: tuple = None,
    cookies: dict = None,
    params: dict = None,
    allow_redirects: bool = False,
    page_id: int = None,
) -> Response:
    response = requests.get(
        url, params=params, auth=auth, cookies=cookies, allow_redirects=allow_redirects
    )
    was_denied = "Access Denied" in response.content.decode("UTF-8")
    if response.status_code == HTTP_200_OK and was_denied:
        print(f"Request to {url} was denied. Will try to re-authorize")
        response = requests.get(response.url, auth=auth, cookies=cookies)
    if response.history and (
        response.status_code in [HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN]
    ):
        print(
            f"Request to {url} was redirected to {response.url} which asked for"
            f" credentials, will try to authorize with basic auth"
        )
        response = requests.get(response.url, auth=auth, cookies=cookies)

    redirect = (
        f"to {response.headers['location']} "
        if response.status_code == HTTP_302_FOUND
        else ""
    )
    page_id = f" -> PAGE ID: {page_id}" if page_id else ""
    msg = f"Expected {status_code} but got {response.status_code} {redirect}from {url}{page_id}"
    assert response.status_code == status_code, msg
    return response


def get_page_ids_by_type(page_type: str) -> Tuple[List[int], int]:
    page_ids = []

    # get first page of results
    relative_url = get_relative_url("cms-api:pages")
    endpoint = f"{relative_url}?type={page_type}"
    response = cms_api_client.get(endpoint)
    total_response_time = response.raw_response.elapsed.total_seconds()
    assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)

    # get IDs of all pages from the response
    content = response.json()
    page_ids += [page["id"] for page in content["items"]]

    total_count = content["meta"]["total_count"]
    if total_count > len(page_ids):
        print(
            f"Found more than {len(content['items'])} pages of {page_type} "
            f"type. Will fetch details of all remaining pages"
        )
    while len(page_ids) < total_count:
        offset = len(page_ids) + len(content["items"])
        endpoint = f"{relative_url}?type={page_type}&offset={offset}"
        response = cms_api_client.get(endpoint)
        total_response_time += response.raw_response.elapsed.total_seconds()
        assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)
        content = response.json()
        page_ids += [page["id"] for page in content["items"]]

    result = list(sorted(page_ids))
    error = f"Expected to get {total_count} IDs but got {len(list(sorted(page_ids)))}"
    assert len(result) == total_count, error
    return result, total_response_time


@retry(wait_fixed=3000, stop_max_attempt_number=3)
def sync_requests(endpoints: List[str]):
    result = []
    for endpoint in endpoints:
        response = cms_api_client.get(endpoint)
        print(
            f"Got response from {response.raw_response.url} in: "
            f"{response.raw_response.elapsed.total_seconds()}s"
        )
        result.append(response)
    return result


def get_pages_types(*, skip: list = None) -> List[str]:
    response = cms_api_client.get(get_relative_url("cms-api:page-types"))
    assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)
    types = response.json()["types"]
    # remove generic (parent) page type common to all pages
    types.remove("wagtailcore.page")
    if skip:
        types = sorted(list(set(types) - set(skip)))
    return types


def get_pages_from_api(page_types: list, *, use_async_client: bool = True) -> dict:
    page_endpoints_by_type = defaultdict(list)
    responses = defaultdict(list)
    base = get_absolute_url("cms-api:pages")

    for page_type in page_types:
        page_ids_of_type, responses_time = get_page_ids_by_type(page_type)
        count = str(len(page_ids_of_type)).rjust(2, " ")
        print(
            f"Found {count} {page_type} pages in {responses_time}s {page_ids_of_type}"
        )
        page_endpoints_by_type[page_type] += [f"{base}{id}/" for id in page_ids_of_type]

    for page_type in page_endpoints_by_type:
        if use_async_client:
            loop = asyncio.get_event_loop()
            responses[page_type] += loop.run_until_complete(
                fetch(page_endpoints_by_type[page_type])
            )
        else:
            responses[page_type] = sync_requests(page_endpoints_by_type[page_type])

    return dict(responses)


def invest_find_draft_urls(responses: dict) -> List[Tuple[str, int]]:
    """
    Invest app includes language code in the endpoint rather than using ?lang=
    query param, thus it requires different processing.
    """
    result = []
    for page_type in responses.keys():
        for response in responses[page_type]:
            page = response.json()
            page_id = page["id"]
            draft_token = page["meta"]["draft_token"]
            if draft_token is not None:
                live_url = check_for_special_page_cases(page)
                parsed = urlparse(live_url)
                languages = response.json()["meta"]["languages"]
                language_codes = [language[0] for language in languages]
                for code in language_codes:
                    if code == "en-gb":
                        url = live_url
                    else:
                        scheme = parsed.scheme
                        netloc = parsed.netloc
                        url = f"{scheme}://{netloc}/{code}{parsed.path}"

                    if should_skip_url(url):
                        continue

                    draft_url = f"{url}?draft_token={draft_token}"
                    draft_url = check_for_special_urls_cases(draft_url)
                    result.append((draft_url, page_id))

    return result


def invest_find_published_translated_urls(responses: dict) -> List[Tuple[str, int]]:
    """
    Invest app includes language code in the endpoint rather than using ?lang=
    query param, thus it requires different processing.
    """
    result = []
    for page_type in responses.keys():
        for response in responses[page_type]:
            if should_skip_never_published_page(response):
                continue
            page_id = response.json()["id"]
            live_url = response.json()["meta"]["url"]
            parsed = urlparse(live_url)
            lang_codes = [lang[0] for lang in response.json()["meta"]["languages"]]
            for code in lang_codes:

                if code == "en-gb":
                    url = live_url
                else:
                    url = f"{parsed.scheme}://{parsed.netloc}/{code}{parsed.path}"

                url = check_for_special_urls_cases(url)
                if should_skip_url(url):
                    continue

                result.append((url, page_id))

    return result


def find_draft_urls(responses: dict) -> List[Tuple[str, int]]:
    result = []
    for page_type in responses.keys():
        for response in responses[page_type]:
            if response.status_code == HTTP_200_OK:
                page = response.json()
                page_id = page["id"]
                draft_token = page["meta"]["draft_token"]
                if draft_token is not None:

                    url = check_for_special_page_cases(page)
                    url = check_for_special_urls_cases(url)
                    if should_skip_url(url):
                        continue

                    draft_url = f"{url}?draft_token={draft_token}"
                    lang_codes = [lang[0] for lang in page["meta"]["languages"]]
                    for code in lang_codes:
                        lang_url = f"{draft_url}&lang={code}"
                        result.append((lang_url, page_id))
            else:
                logging.error(
                    f"Expected 200 but got {response.status_code} from "
                    f"{response.raw_response.url}"
                )
    return result


def find_published_urls(responses: dict) -> List[Tuple[str, int]]:
    result = []
    for page_type in responses.keys():
        for response in responses[page_type]:
            if should_skip_never_published_page(response):
                continue
            page = response.json()
            page_id = page["id"]
            url = check_for_special_page_cases(page)
            url = check_for_special_urls_cases(url)
            if should_skip_url(url):
                continue

            result.append((url, page_id))
    return result


def find_published_translated_urls(responses: dict) -> List[Tuple[str, int]]:
    result = []
    for page_type in responses.keys():
        for response in responses[page_type]:
            if should_skip_never_published_page(response):
                continue
            page = response.json()
            page_id = page["id"]

            url = check_for_special_page_cases(page)
            url = check_for_special_urls_cases(url)
            if should_skip_url(url):
                continue

            lang_codes = [lang[0] for lang in page["meta"]["languages"]]
            for code in lang_codes:
                result.append(("{}?lang={}".format(url, code), page_id))
    return result
