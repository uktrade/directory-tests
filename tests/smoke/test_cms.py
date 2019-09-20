# -*- coding: utf-8 -*-
import pytest
from directory_cms_client.client import cms_api_client
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from directory_tests_shared import URLs
from directory_tests_shared.settings import DIRECTORY_CMS_API_CLIENT_BASE_URL
from tests.smoke.cms_api_helpers import (
    find_draft_urls,
    find_published_translated_urls,
    find_published_urls,
    get_and_assert,
    get_pages_from_api,
    get_pages_types,
    status_error,
)

SKIPPED_PAGE_TYPES = [
    "wagtailcore.page"  # remove generic (parent) page type common to all pages
]
if "dev" in DIRECTORY_CMS_API_CLIENT_BASE_URL:
    SKIPPED_PAGE_TYPES += [
        "export_readiness.homepage",  # 500 ISE
        "great_international.capitalinvestopportunitypage",  # 502 timeout
        # ignore sub-sector pages as they're behind a feature flag
        # and are used to categorise capital invest opportunities
        # so come up as a filter on the opportunity listing page
        "great_international.internationalsubsectorpage",
    ]
if "staging" in DIRECTORY_CMS_API_CLIENT_BASE_URL:
    SKIPPED_PAGE_TYPES += [
        "export_readiness.articlelistingpage",  # 500 ISE
        "great_international.internationalarticlepage",  # 500 ISE
        "great_international.internationalcampaignpage",  # 500 ISE
    ]
if "uat" in DIRECTORY_CMS_API_CLIENT_BASE_URL:
    SKIPPED_PAGE_TYPES += [
        "great_international.baseinternationalsectorpage"  # 400 not found
    ]

ALL_PAGE_TYPES = get_pages_types(skip=SKIPPED_PAGE_TYPES)

EXRED_PAGE_TYPES = [t for t in ALL_PAGE_TYPES if t.startswith("export_readiness.")]
INTERNATIONAL_PAGE_TYPES = [
    t for t in ALL_PAGE_TYPES if t.startswith("great_international.")
]

EXRED_PAGES = get_pages_from_api(EXRED_PAGE_TYPES, use_async_client=False)
INTERNATIONAL_PAGES = get_pages_from_api(
    INTERNATIONAL_PAGE_TYPES, use_async_client=False
)

ALL_PAGES = {}
ALL_PAGES.update(EXRED_PAGES)
ALL_PAGES.update(INTERNATIONAL_PAGES)


@pytest.mark.parametrize(
    "relative_url", [URLs.CMS_API_IMAGES.relative, URLs.CMS_API_DOCUMENTS.relative]
)
def test_wagtail_get_disabled_content_endpoints(relative_url):
    response = cms_api_client.get(relative_url)
    assert response.status_code == HTTP_404_NOT_FOUND, status_error(
        HTTP_404_NOT_FOUND, response
    )


def test_wagtail_get_pages():
    endpoint = URLs.CMS_API_PAGES.relative
    response = cms_api_client.get(endpoint)
    assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)


@pytest.mark.parametrize("limit", [2, 10, 20])
def test_wagtail_get_number_of_pages(limit):
    query = "?order=id&limit={}".format(limit)
    endpoint = URLs.CMS_API_PAGES.relative + query
    response = cms_api_client.get(endpoint)
    assert len(response.json()["items"]) == limit


def test_wagtail_can_list_only_20_pages():
    query = "?limit=21"
    endpoint = URLs.CMS_API_PAGES.relative + query
    response = cms_api_client.get(endpoint)
    assert response.json()["message"] == "limit cannot be higher than 20"


@pytest.mark.dev
@pytest.mark.parametrize(
    "application", ["Components", "Great Domestic pages", "Great International pages"]
)
def test_wagtail_get_pages_per_application_on_dev(application):
    # Get ID of specific application (parent page)
    query = "?title={}".format(application)
    endpoint = URLs.CMS_API_PAGES.relative + query
    response = cms_api_client.get(endpoint)
    assert response.json()["meta"]["total_count"] == 1
    application_id = response.json()["items"][0]["id"]

    # Get inf about its child pages
    query = "?child_of={}".format(application_id)
    endpoint = URLs.CMS_API_PAGES.relative + query
    response = cms_api_client.get(endpoint)
    assert response.json()["meta"]["total_count"] > 0


@pytest.mark.stage
@pytest.mark.parametrize(
    "application", ["Components", "Great Domestic pages", "great.gov.uk international"]
)
def test_wagtail_get_pages_per_application_on_stage(application):
    test_wagtail_get_pages_per_application_on_dev(application)


@pytest.mark.prod
@pytest.mark.parametrize(
    "application", ["Components", "great.gov.uk", "great.gov.uk international"]
)
def test_wagtail_get_pages_per_application_on_prod(application):
    test_wagtail_get_pages_per_application_on_dev(application)


@pytest.mark.parametrize("url, page_id", find_published_urls(ALL_PAGES))
def test_all_published_english_pages_should_return_200(url, page_id, basic_auth):
    get_and_assert(
        url, HTTP_200_OK, auth=basic_auth, allow_redirects=True, page_id=page_id
    )


@pytest.mark.parametrize("url, page_id", find_published_translated_urls(ALL_PAGES))
def test_published_translated_pages_should_return_200_new(url, page_id, basic_auth):
    get_and_assert(
        url, HTTP_200_OK, auth=basic_auth, allow_redirects=True, page_id=page_id
    )


@pytest.mark.parametrize("url, page_id", find_draft_urls(ALL_PAGES))
def test_drafts_of_translated_pages_should_return_200_new(url, page_id, basic_auth):
    get_and_assert(url, HTTP_200_OK, auth=basic_auth, page_id=page_id)
