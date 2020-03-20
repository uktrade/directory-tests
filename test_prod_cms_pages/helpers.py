# -*- coding: utf-8 -*-
from pprint import pformat
from typing import List, Tuple

import requests
from django.conf import settings
from envparse import env
from requests import Response
from requests.exceptions import (
    ChunkedEncodingError,
    ConnectionError,
    ConnectTimeout,
    ContentDecodingError,
    HTTPError,
    InvalidHeader,
    InvalidSchema,
    InvalidURL,
    MissingSchema,
    ProxyError,
    ReadTimeout,
    RequestException,
    RetryError,
    SSLError,
    StreamConsumedError,
    Timeout,
    TooManyRedirects,
    UnrewindableBodyError,
    URLRequired,
)
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_302_FOUND,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
)
from termcolor import cprint
from urllib3.exceptions import HTTPError as BaseHTTPError

#####################################################################
# CMS API client configuration
#####################################################################
CMS_API_KEY = env.str("CMS_API_KEY")
CMS_API_URL = env.str("CMS_API_URL")
settings.configure(
    DIRECTORY_CMS_API_CLIENT_API_KEY=CMS_API_KEY,
    DIRECTORY_CMS_API_CLIENT_BASE_URL=CMS_API_URL,
    DIRECTORY_CMS_API_CLIENT_CACHE_EXPIRE_SECONDS=60 * 60 * 24 * 30,
    DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT=60,
    DIRECTORY_CMS_API_CLIENT_SENDER_ID="directory",
    DIRECTORY_CMS_API_CLIENT_SERVICE_NAME="EXPORT_READINESS",
    CACHES={
        "cms_fallback": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake",
        },
    },
)


REQUEST_EXCEPTIONS = (
    BaseHTTPError,
    RequestException,
    HTTPError,
    ConnectionError,
    ProxyError,
    SSLError,
    Timeout,
    ConnectTimeout,
    ReadTimeout,
    URLRequired,
    TooManyRedirects,
    MissingSchema,
    InvalidSchema,
    InvalidURL,
    InvalidHeader,
    ChunkedEncodingError,
    ContentDecodingError,
    StreamConsumedError,
    RetryError,
    UnrewindableBodyError,
)


def blue(x: str):
    """Print out a message in blue to console."""
    cprint(x, "blue", attrs=["bold"])


def red(x: str):
    """Print out a message in red to console."""
    cprint(x, "red", attrs=["bold"])


def camel_case_to_separate_words(camel_case_string: str) -> str:
    """Convert CamelCase string into a string with words separated by spaces"""
    words = [[camel_case_string[0]]]

    for character in camel_case_string[1:]:
        if words[-1][-1].islower() and character.isupper():
            words.append(list(character))
        else:
            words[-1].append(character)

    return " ".join("".join(word) for word in words)


def check_for_special_urls_cases(url: str) -> str:
    # this was added because of BUG CMS-1426
    if "setup-guides" in url:
        url = url.replace("setup-guides", "uk-setup-guide")
    if "setup-guide-landing" in url:
        url = url.replace("setup-guide-landing", "uk-setup-guide")
    if "setup-guide-landing-page/" in url:
        url = url.replace("setup-guide-landing-page/", "")
    if "uk-setup-guide-page/" in url:
        url = url.replace("uk-setup-guide-page/", "")
    if "performance-dashboard-" in url:
        url = url.replace("performance-dashboard-", "performance-dashboard/")
    if "high-potential-opportunity-submit-success" in url:
        url = url.replace("high-potential-opportunity-submit-success", "success")
    if "high-potential-opportunitiesrailcontact" in url:
        url = url.replace(
            "high-potential-opportunitiesrailcontact",
            "high-potential-opportunities/rail/contact",
        )
    if "industriescontact/" in url:
        url = url.replace("industriescontact/", "industries/contact/")
    if "industry-contact/" in url:
        url = url.replace("industry-contact/", "")
    # International pages which are not handled by UI are available via
    # "/content/" infix
    if (
        "/international/" in url
        and not url.endswith("/international/")
        and "/international/content/" not in url
        and "/content/how-to-setup-in-the-uk/" not in url
        and "/campaigns/" not in url
        and "/international-eu-exit-news/" not in url
    ):
        url = url.replace("/international/", "/international/content/")
    if "/international/content/success/" in url:
        url = url.replace("/international/content/success/", "/international/success/")
    if url.startswith("http://"):
        url = url.replace("http://", "https://")
    return url


def check_for_special_page_cases(page: dict) -> str:
    if page["page_type"] in [
        "ArticlePage",
        "ArticleListingPage",
        "SuperregionPage",
        "CountryGuidePage",
    ]:
        url = check_for_special_urls_cases(page["full_url"])
    elif page["page_type"] in [
        "InvestHomePage",
        "LandingPage",
        "HomePage",
        "InternationalLandingPage",
    ]:
        # All draft version of pages that use CMS components are affected by bug CMS-754
        # invest homepage
        # fas homepage
        # International page
        # domestic eu-exit-news list
        skip_full_paths = [
            "/home-page/",  # Invest home page
            "/landing-page/",  # FAS home page
            "/home/",  # Domestic home page
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


def should_skip_url(url: str) -> bool:
    skip = [
        "/markets/",  # ATM there's no landing page for markets
        "/asia-pacific/",  #
        "country-guides",  # Country guides are not ready for testing
        "/international-eu-exit-news/",  # International EU Exit news aren't enabled
        "/eu-exit-news/",  # International news aren't always enabled
        "contact/find-uk-companies/success/",  # this page is not in use anymore
        "skip.this.url",  # skip URL which was deemed to skip the page checker
        "/success-stories/",  # Success Stories are behind a feature flag
        # these 2 contact forms were never released
        "/department-for-environment-food-and-rural-affairs/",
        "/department-for-business-energy-and-industrial-strategy/",
    ]
    if any(True for bit in skip if bit in url):
        return True

    skip_endings = [
        "uk-regions/",  # this was added because of CMS-413
        "uk-regions",  # there's no landing page for UK Regions
    ]
    if any(True for bit in skip_endings if url.endswith(bit)):
        return True
    if not url.startswith("http"):  # skip invalid URLs (e.g. for component pages)
        return True

    return False


def status_error(expected_status_code: int, response: Response) -> str:
    if isinstance(response, Response):
        return (
            f"{response.request.method} {response.url} "
            f"returned {response.status_code} instead of expected "
            f"{expected_status_code}\n"
            f"REQ headers: {pformat(response.request.headers)}\n"
            f"RSP headers: {pformat(response.headers)}"
        )
    else:
        raise RuntimeError(f"Got an unknown type of response {type(response)}")


def get_and_assert(
    url: str,
    status_code: int,
    *,
    auth: tuple = None,
    cookies: dict = None,
    params: dict = None,
    allow_redirects: bool = False,
    page_id: int = None,
    headers: dict = None,
) -> Response:
    response = requests.get(
        url,
        params=params,
        auth=auth,
        cookies=cookies,
        allow_redirects=allow_redirects,
        headers=headers,
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
        response = requests.get(
            response.url, auth=auth, cookies=cookies, headers=headers
        )

    redirect = (
        f"to {response.headers['location']} "
        if response.status_code == HTTP_302_FOUND
        else ""
    )
    page_id = f" -> PAGE ID: {page_id}" if page_id else ""
    msg = f"Expected {status_code} but got {response.status_code} {redirect}from {url}{page_id}"
    assert response.status_code == status_code, msg
    return response


def find_draft_urls(pages: List[dict]) -> List[Tuple[str, int]]:
    result = []
    for page in pages:
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
    return result


def find_published_urls(pages: List[dict]) -> List[Tuple[str, int]]:
    result = []
    for page in pages:
        page_id = page["id"]
        url = check_for_special_page_cases(page)
        url = check_for_special_urls_cases(url)
        if should_skip_url(url):
            continue
        result.append((url, page_id))
    return result


def find_published_translated_urls(pages: List[dict]) -> List[Tuple[str, int]]:
    result = []
    for page in pages:
        page_id = page["id"]

        url = check_for_special_page_cases(page)
        url = check_for_special_urls_cases(url)
        if should_skip_url(url):
            continue

        lang_codes = [lang[0] for lang in page["meta"]["languages"]]
        for code in lang_codes:
            result.append(("{}?lang={}".format(url, code), page_id))
    return result


def get_pks_by_page_type(page_type: str) -> List[int]:
    from directory_cms_client.client import cms_api_client  # NOQA

    result = []
    try:
        response = cms_api_client.get(f"api/pages/?type={page_type}")
    except requests.exceptions.HTTPError as ex:
        red(f"GET api/pages/?type={page_type} -> Failed because of: {ex}")
    else:
        if response.status_code != HTTP_200_OK:
            red(
                f"GET api/pages/?type={page_type} -> {response.status_code} {response.reason}"
            )
        else:
            result = response.json()
            error = (
                f"Expected response from 'GET api/pages/?type={page_type}' to be a "
                f"List[int] not {type(result)}"
            )
            assert all(isinstance(val, int) for val in result), error
    print(f"GET api/pages/?type={page_type} -> {result}")
    return result


def get_page_by_pk(pk: int) -> dict:
    from directory_cms_client.client import cms_api_client  # NOQA

    result = {}
    try:
        response = cms_api_client.get(f"api/pages/{pk}/")
    except requests.exceptions.HTTPError as ex:
        red(f"GET api/pages/{pk}/ -> Failed because of: {ex}")
    else:
        if response.status_code != 200:
            red(f"GET api/pages/{pk}/ -> {response.status_code} {response.reason}")
        elif response.status_code == HTTP_204_NO_CONTENT:
            blue(
                f"GET {response.url} -> {response.status_code} {response.reason} "
                f"in: {response.elapsed.total_seconds()}s EMPTY RESPONSE"
            )
        else:
            result = response.json()
    return result


def all_cms_pks() -> List[int]:
    from directory_cms_client.client import cms_api_client  # NOQA

    response = cms_api_client.get("api/pages/")
    assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)
    pks = response.json()
    print(f"\nCMS returned {len(pks)} PKs of published pages")
    return pks


def fetch_url(endpoint: str) -> Response:
    from directory_cms_client.client import cms_api_client  # NOQA

    response = None
    try:
        response = cms_api_client.get(endpoint)
    except REQUEST_EXCEPTIONS as ex:
        red(f"GET {endpoint} -> Failed because of: {ex}")
    else:
        if response.status_code == 200:
            print(f"GET {response.url} -> {response.status_code} {response.reason}")
        else:
            red(f"GET {response.url} -> {response.status_code} {response.reason}")
    return response


def parallel_requests(page_endpoints: List[str]) -> Tuple[List[dict], List[Response]]:
    """Fetch pages in parallel using multiple workers.
    SRC: https://stackoverflow.com/a/54878794
    """
    from concurrent.futures import ThreadPoolExecutor

    pool = ThreadPoolExecutor(max_workers=2)
    responses = [r for r in pool.map(fetch_url, page_endpoints) if r]
    ok_pages = [r.json() for r in responses if r.status_code == HTTP_200_OK]
    bad_responses = [r for r in responses if r.status_code != HTTP_200_OK]
    return ok_pages, bad_responses


def get_pages_by_pk(
    page_pks: list, *, use_parallel_requests: bool = True
) -> Tuple[List[dict], List[Response]]:
    """Gets all pages by PKs.

    Returns: a list of working pages and a list of bad responses (non 200 OK)
    """
    page_endpoints = ["api/pages/{page_id}/".format(page_id=pk) for pk in page_pks]

    ok_pages, bad_responses = parallel_requests(page_endpoints)

    return ok_pages, bad_responses
