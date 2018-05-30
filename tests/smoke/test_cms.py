import http.client

import pytest
import requests

from tests import get_absolute_url, get_relative_url
from tests.settings import DIRECTORY_API_HEALTH_CHECK_TOKEN as TOKEN


def test_healthcheck_ping_endpoint(cms_client):
    endpoint = get_relative_url('cms-healthcheck:ping')
    response = cms_client.get(endpoint)
    assert response.status_code == http.client.OK


@pytest.mark.skip(reason="check ticket: CMS-146")
def test_healthcheck_database_endpoint():
    params = {'token': TOKEN}
    absolute_url = get_absolute_url('cms-healthcheck:database')
    response = requests.get(absolute_url, params=params)
    error_msg = (
        "Expected 200 but got {}\n{}".format(
            response.status_code, response.content.decode("utf-8")))
    assert response.status_code == http.client.OK, error_msg


@pytest.mark.parametrize("relative_url", [
    get_relative_url('cms-api:images'),
    get_relative_url('cms-api:documents'),
])
def test_wagtail_get_disabled_content_endpoints(cms_client, relative_url):
    response = cms_client.get(relative_url)
    assert response.status_code == http.client.NOT_FOUND


def test_wagtail_get_pages(cms_client):
    response = cms_client.get(get_relative_url('cms-api:pages'))
    assert response.status_code == http.client.OK


@pytest.mark.parametrize("slug", [
    "landing-page",
    "industry-contact",
    "industries-landing-page",
    "get-finance",
    "terms-and-conditions",
    "privacy-and-cookies",
    "legal-services",
])
def test_wagtail_get_page_by_slug(cms_client, slug):
    relative_url = get_relative_url('cms-api:pages-by-slug').format(slug)
    response = cms_client.get(relative_url)
    assert response.status_code == http.client.OK
    assert response.json()["meta"]["slug"] == slug


@pytest.mark.parametrize("page", [
    ("find_a_supplier.IndustryPage", None),
    ("find_a_supplier.IndustryArticlePage", None),
    ("find_a_supplier.LandingPage", "Find a supplier - homepage"),
    ("find_a_supplier.IndustryContactPage", "Contact us"),
    ("export_readiness.TermsAndConditionsPage", "Terms and Conditions"),
    ("export_readiness.PrivacyAndCookiesPage", "Privacy and cookies"),
    ("export_readiness.GetFinancePage", "Get finance"),
])
def test_wagtail_get_page_by_type(cms_client, page):
    model, title = page
    relative_url = get_relative_url('cms-api:pages-by-type').format(model)
    response = cms_client.get(relative_url)
    assert response.status_code == http.client.OK
    if title:
        assert response.json()["title"] == title


@pytest.mark.parametrize("limit", [
    2,
    10,
    20,
])
def test_wagtail_get_number_of_pages(cms_client, limit):
    query = "?order=id&limit={}".format(limit)
    relative_url = get_relative_url('cms-api:pages') + query
    response = cms_client.get(relative_url)
    assert len(response.json()["items"]) == limit


@pytest.mark.parametrize("application", [
    "Export Readiness pages",
    "Find a Supplier Pages"
])
def test_wagtail_get_pages_per_application(cms_client, application):
    # Get ID of specific application (parent page)
    query = "?title={}".format(application)
    relative_url = get_relative_url('cms-api:pages') + query
    response = cms_client.get(relative_url)
    assert response.json()["meta"]["total_count"] == 1
    application_id = response.json()["items"][0]["id"]

    # Get inf about its child pages
    query = "?child_of={}".format(application_id)
    relative_url = get_relative_url('cms-api:pages') + query
    response = cms_client.get(relative_url)
    assert response.json()["meta"]["total_count"] > 0
