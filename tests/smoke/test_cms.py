# -*- coding: utf-8 -*-
import pytest
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

import allure
from directory_tests_shared import URLs
from directory_tests_shared.clients import CMS_API_CLIENT
from tests.smoke.cms_api_helpers import (
    all_cms_pks,
    find_draft_urls,
    find_published_translated_urls,
    find_published_urls,
    get_and_assert,
    get_pages_by_pk,
    status_error,
)

pytestmark = [allure.suite("CMS"), allure.feature("CMS")]


ALL_OK_PAGES, ALL_BAD_RESPONSES = get_pages_by_pk(all_cms_pks())


@pytest.mark.parametrize(
    "relative_url", [URLs.CMS_API_IMAGES.relative, URLs.CMS_API_DOCUMENTS.relative]
)
def test_wagtail_get_disabled_content_endpoints(relative_url):
    response = CMS_API_CLIENT.get(relative_url)
    assert response.status_code == HTTP_404_NOT_FOUND, status_error(
        HTTP_404_NOT_FOUND, response
    )


def test_wagtail_get_pages():
    endpoint = URLs.CMS_API_PAGES.relative
    response = CMS_API_CLIENT.get(endpoint)
    assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)


@pytest.mark.dev
@pytest.mark.parametrize(
    "application", ["Components", "Great Domestic pages", "Great International pages"]
)
def test_wagtail_get_pages_per_application_on_dev(application):
    # Get ID of specific application (parent page)
    query = "?title={}".format(application)
    endpoint = URLs.CMS_API_PAGES.relative + query
    response = CMS_API_CLIENT.get(endpoint)
    assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)
    assert response.json()
    application_id = response.json()[0]

    # Get inf about its child pages
    query = "?child_of={}".format(application_id)
    endpoint = URLs.CMS_API_PAGES.relative + query
    response = CMS_API_CLIENT.get(endpoint)
    assert len(response.json()) > 0


@pytest.mark.stage
@pytest.mark.parametrize(
    "application", ["Components", "Great Domestic pages", "Great International pages"]
)
def test_wagtail_get_pages_per_application_on_stage(application):
    test_wagtail_get_pages_per_application_on_dev(application)


@pytest.mark.uat
@pytest.mark.parametrize(
    "application", ["Components", "great.gov.uk", "Welcome to great.gov.uk"]
)
def test_wagtail_get_pages_per_application_on_uat(application):
    test_wagtail_get_pages_per_application_on_dev(application)


@pytest.mark.prod
@pytest.mark.parametrize(
    "application", ["Components", "great.gov.uk", "great.gov.uk international"]
)
def test_wagtail_get_pages_per_application_on_prod(application):
    test_wagtail_get_pages_per_application_on_dev(application)


@pytest.mark.parametrize("url, page_id", find_published_urls(ALL_OK_PAGES))
def test_all_published_english_pages_should_return_200(url, page_id, basic_auth):
    get_and_assert(
        url, HTTP_200_OK, auth=basic_auth, allow_redirects=True, page_id=page_id
    )


@pytest.mark.parametrize("url, page_id", find_published_translated_urls(ALL_OK_PAGES))
def test_published_translated_pages_should_return_200_new(url, page_id, basic_auth):
    get_and_assert(
        url, HTTP_200_OK, auth=basic_auth, allow_redirects=True, page_id=page_id
    )


@pytest.mark.parametrize("url, page_id", find_draft_urls(ALL_OK_PAGES))
def test_drafts_of_translated_pages_should_return_200_new(url, page_id, basic_auth):
    get_and_assert(url, HTTP_200_OK, auth=basic_auth, page_id=page_id)
