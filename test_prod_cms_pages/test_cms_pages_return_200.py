# -*- coding: utf-8 -*-
import pytest
from rest_framework.status import HTTP_200_OK

from helpers import (
    all_cms_pks,
    find_draft_urls,
    find_published_translated_urls,
    find_published_urls,
    get_and_assert,
    get_pages_by_pk,
)

ALL_OK_PAGES, ALL_BAD_RESPONSES = get_pages_by_pk(all_cms_pks())


@pytest.mark.parametrize("url, page_id", find_published_urls(ALL_OK_PAGES))
def test_all_published_english_pages_should_return_200(url, page_id):
    get_and_assert(url, HTTP_200_OK, allow_redirects=True, page_id=page_id)


@pytest.mark.parametrize("url, page_id", find_published_translated_urls(ALL_OK_PAGES))
def test_published_translated_pages_should_return_200(url, page_id):
    get_and_assert(url, HTTP_200_OK, allow_redirects=True, page_id=page_id)


@pytest.mark.parametrize("url, page_id", find_draft_urls(ALL_OK_PAGES))
def test_drafts_of_translated_pages_should_return_200(url, page_id):
    get_and_assert(url, HTTP_200_OK, allow_redirects=True, page_id=page_id)
