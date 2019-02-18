import http.client

import pytest
from directory_cms_client.client import cms_api_client
from directory_constants.constants import cms as SERVICE_NAMES
from retrying import retry

from tests import get_relative_url, retriable_error
from tests.smoke.cms_api_helpers import (
    find_draft_urls,
    find_published_translated_urls,
    find_published_urls,
    get_and_assert,
    get_pages_from_api,
    get_pages_types,
    invest_find_draft_urls,
    invest_find_published_translated_urls,
    status_error,
)

SKIPPED_PAGE_TYPES = []

ALL_PAGE_TYPES = get_pages_types(skip=SKIPPED_PAGE_TYPES)

EXRED_PAGE_TYPES = [t for t in ALL_PAGE_TYPES if t.startswith('export_readiness.')]
INVEST_PAGE_TYPES = [t for t in ALL_PAGE_TYPES if t.startswith('invest.')]
FAS_PAGE_TYPES = [t for t in ALL_PAGE_TYPES if t.startswith('find_a_supplier.')]
COMPONENTS_PAGE_TYPES = [t for t in ALL_PAGE_TYPES if t.startswith('components.')]

INVEST_PAGES = get_pages_from_api(INVEST_PAGE_TYPES, use_async_client=False)
FAS_PAGES = get_pages_from_api(FAS_PAGE_TYPES, use_async_client=False)
EXRED_PAGES = get_pages_from_api(EXRED_PAGE_TYPES, use_async_client=False)

ALL_PAGES = {}
ALL_PAGES.update(INVEST_PAGES)
ALL_PAGES.update(FAS_PAGES)
ALL_PAGES.update(EXRED_PAGES)

NON_INVEST_API_PAGES = {}
NON_INVEST_API_PAGES.update(FAS_PAGES)
NON_INVEST_API_PAGES.update(EXRED_PAGES)


@pytest.mark.parametrize(
    "relative_url",
    [
        get_relative_url("cms-api:images"),
        get_relative_url("cms-api:documents"),
    ],
)
def test_wagtail_get_disabled_content_endpoints(relative_url):
    response = cms_api_client.get(relative_url)
    assert response.status_code == http.client.NOT_FOUND, status_error(
        http.client.NOT_FOUND, response
    )


def test_wagtail_get_pages():
    endpoint = get_relative_url("cms-api:pages")
    response = cms_api_client.get(endpoint)
    assert response.status_code == http.client.OK, status_error(
        http.client.OK, response
    )


@pytest.mark.parametrize("limit", [2, 10, 20])
def test_wagtail_get_number_of_pages(limit):
    query = "?order=id&limit={}".format(limit)
    endpoint = get_relative_url("cms-api:pages") + query
    response = cms_api_client.get(endpoint)
    assert len(response.json()["items"]) == limit


def test_wagtail_can_list_only_20_pages():
    query = "?limit=21"
    endpoint = get_relative_url("cms-api:pages") + query
    response = cms_api_client.get(endpoint)
    assert response.json()["message"] == "limit cannot be higher than 20"


@pytest.mark.parametrize(
    "application", [
        "Great Domestic pages",
        "Find a Supplier Pages",
        "Invest pages",
        "Components"
    ]
)
def test_wagtail_get_pages_per_application_on_dev(application):
    # Get ID of specific application (parent page)
    query = "?title={}".format(application)
    endpoint = get_relative_url("cms-api:pages") + query
    response = cms_api_client.get(endpoint)
    assert response.json()["meta"]["total_count"] == 1
    application_id = response.json()["items"][0]["id"]

    # Get inf about its child pages
    query = "?child_of={}".format(application_id)
    endpoint = get_relative_url("cms-api:pages") + query
    response = cms_api_client.get(endpoint)
    assert response.json()["meta"]["total_count"] > 0


@pytest.mark.parametrize("url", find_published_urls(ALL_PAGES))
def test_all_published_english_pages_should_return_200(url, basic_auth):
    get_and_assert(url, 200, auth=basic_auth)


@pytest.mark.parametrize(
    "url", find_published_translated_urls(NON_INVEST_API_PAGES)
)
def test_non_invest_published_translated_pages_should_return_200_new(url, basic_auth):
    get_and_assert(url, 200, auth=basic_auth)


@pytest.mark.parametrize("url", find_draft_urls(NON_INVEST_API_PAGES))
def test_non_invest_draft_translated_pages_should_return_200_new(url, basic_auth):
    get_and_assert(url, 200, auth=basic_auth)


@pytest.mark.parametrize(
    "url", invest_find_published_translated_urls(INVEST_PAGES)
)
def test_published_translated_invest_pages_should_return_200_new(url, basic_auth):
    get_and_assert(url, 200, auth=basic_auth)


@pytest.mark.parametrize("url", invest_find_draft_urls(INVEST_PAGES))
def test_draft_translated_invest_pages_should_return_200_new(url, basic_auth):
    get_and_assert(url, 200, auth=basic_auth)


@retry(
    wait_fixed=30000,
    stop_max_attempt_number=2,
    retry_on_exception=retriable_error,
)
@pytest.mark.parametrize(
    "service_name, slug",
    [
        (SERVICE_NAMES.EXPORT_READINESS, "get-finance"),
        (SERVICE_NAMES.EXPORT_READINESS, "terms-and-conditions"),
        (SERVICE_NAMES.EXPORT_READINESS, "privacy-and-cookies"),
        (SERVICE_NAMES.EXPORT_READINESS, "performance-dashboard"),
        (SERVICE_NAMES.EXPORT_READINESS, "performance-dashboard-notes"),
        (SERVICE_NAMES.EXPORT_READINESS, "performance-dashboard-invest"),
        (
            SERVICE_NAMES.EXPORT_READINESS,
            "performance-dashboard-trade-profiles",
        ),
        (
            SERVICE_NAMES.EXPORT_READINESS,
            "performance-dashboard-selling-online-overseas",
        ),
        (
            SERVICE_NAMES.EXPORT_READINESS,
            "performance-dashboard-export-opportunities",
        ),
        (SERVICE_NAMES.FIND_A_SUPPLIER, "landing-page"),
        (SERVICE_NAMES.FIND_A_SUPPLIER, "industry-contact"),
        (SERVICE_NAMES.FIND_A_SUPPLIER, "industries-landing-page"),
        (SERVICE_NAMES.FIND_A_SUPPLIER, "aerospace"),
        (SERVICE_NAMES.FIND_A_SUPPLIER, "agritech"),
        (SERVICE_NAMES.FIND_A_SUPPLIER, "consumer-retail"),
        (SERVICE_NAMES.FIND_A_SUPPLIER, "creative-services"),
        (SERVICE_NAMES.FIND_A_SUPPLIER, "cyber-security"),
        (SERVICE_NAMES.FIND_A_SUPPLIER, "food-and-drink"),
        (SERVICE_NAMES.FIND_A_SUPPLIER, "healthcare"),
        (SERVICE_NAMES.FIND_A_SUPPLIER, "legal-services"),
        (SERVICE_NAMES.FIND_A_SUPPLIER, "life-sciences"),
        (SERVICE_NAMES.FIND_A_SUPPLIER, "sports-economy"),
        (SERVICE_NAMES.FIND_A_SUPPLIER, "technology"),
        (SERVICE_NAMES.INVEST, "home-page"),
        (SERVICE_NAMES.INVEST, "sector-landing-page"),
        (SERVICE_NAMES.INVEST, "advanced-manufacturing"),
        (SERVICE_NAMES.INVEST, "aerospace"),
        (SERVICE_NAMES.INVEST, "agri-tech"),
        (SERVICE_NAMES.INVEST, "asset-management"),
        (SERVICE_NAMES.INVEST, "automotive"),
        (SERVICE_NAMES.INVEST, "automotive-research-and-development"),
        (SERVICE_NAMES.INVEST, "automotive-supply-chain"),
        (SERVICE_NAMES.INVEST, "capital-investment"),
        (SERVICE_NAMES.INVEST, "chemicals"),
        (SERVICE_NAMES.INVEST, "creative-content-and-production"),
        (SERVICE_NAMES.INVEST, "creative-industries"),
        (SERVICE_NAMES.INVEST, "data-analytics"),
        (SERVICE_NAMES.INVEST, "digital-media"),
        (SERVICE_NAMES.INVEST, "electrical-networks"),
        (SERVICE_NAMES.INVEST, "energy"),
        (SERVICE_NAMES.INVEST, "energy-waste"),
        (SERVICE_NAMES.INVEST, "financial-services"),
        (SERVICE_NAMES.INVEST, "financial-technology"),
        (SERVICE_NAMES.INVEST, "food-and-drink"),
        (SERVICE_NAMES.INVEST, "food-service-and-catering"),
        (SERVICE_NAMES.INVEST, "free-foods"),
        (SERVICE_NAMES.INVEST, "health-and-life-sciences"),
        (SERVICE_NAMES.INVEST, "meat-poultry-and-dairy"),
        (SERVICE_NAMES.INVEST, "medical-technology"),
        (SERVICE_NAMES.INVEST, "motorsport"),
        (SERVICE_NAMES.INVEST, "nuclear-energy"),
        (SERVICE_NAMES.INVEST, "offshore-wind-energy"),
        (SERVICE_NAMES.INVEST, "oil-and-gas"),
        (SERVICE_NAMES.INVEST, "pharmaceutical-manufacturing"),
        (SERVICE_NAMES.INVEST, "retail"),
        (SERVICE_NAMES.INVEST, "technology"),
        (SERVICE_NAMES.INVEST, "uk-region-landing-page"),
        (SERVICE_NAMES.INVEST, "london"),
        (SERVICE_NAMES.INVEST, "north-england"),
        (SERVICE_NAMES.INVEST, "northern-ireland"),
        (SERVICE_NAMES.INVEST, "scotland"),
        (SERVICE_NAMES.INVEST, "south-england"),
        (SERVICE_NAMES.INVEST, "wales"),
        (SERVICE_NAMES.INVEST, "setup-guide-landing-page"),
        (SERVICE_NAMES.INVEST, "apply-uk-visa"),
        (SERVICE_NAMES.INVEST, "establish-base-business-uk"),
        (SERVICE_NAMES.INVEST, "hire-skilled-workers-your-uk-operations"),
        (SERVICE_NAMES.INVEST, "open-uk-business-bank-account"),
        (SERVICE_NAMES.INVEST, "setup-your-business-uk"),
        (SERVICE_NAMES.INVEST, "understand-uk-tax-and-incentives"),
    ],
)
def test_wagtail_get_page_by_slug(cms_client, service_name, slug):
    """Check - https://uktrade.atlassian.net/browse/CMS-412"""
    response = cms_client.lookup_by_slug(slug, service_name=service_name)
    assert response.status_code == http.client.OK, status_error(
        http.client.OK, response
    )
    assert response.json()["meta"]["slug"] == slug


@pytest.mark.parametrize(
    "service_name, slug",
    [
        (SERVICE_NAMES.COMPONENTS, "eu-exit-banner-domestic"),
        (SERVICE_NAMES.COMPONENTS, "eu-exit-banner-international"),
        # (SERVICE_NAMES.COMPONENTS, "international-eu-exit-news"),  # See CMS-754
    ],
)
def test_wagtail_get_component_pages(cms_client, service_name, slug):
    """Check - https://uktrade.atlassian.net/browse/CMS-412"""
    response = cms_client.lookup_by_slug(slug, service_name=service_name)
    assert response.status_code == http.client.OK, status_error(
        http.client.OK, response
    )
    assert response.json()["meta"]["slug"] == slug


@pytest.mark.parametrize("url", find_published_urls(ALL_PAGES))
def test_new_all_published_english_pages_should_return_200(url, basic_auth):
    get_and_assert(url, 200, auth=basic_auth)
