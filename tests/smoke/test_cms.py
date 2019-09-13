import pytest
from directory_cms_client.client import cms_api_client
from directory_constants import cms as SERVICE_NAMES
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from retrying import retry

from tests import retriable_error, URLs, DIRECTORY_CMS_API_CLIENT_BASE_URL
from tests.smoke.cms_api_helpers import (
    find_draft_urls,
    find_published_translated_urls,
    find_published_urls,
    get_and_assert,
    get_pages_from_api,
    get_pages_types,
    status_error,
)

SKIPPED_PAGE_TYPES = []
if "dev" in DIRECTORY_CMS_API_CLIENT_BASE_URL:
    SKIPPED_PAGE_TYPES = [
        "export_readiness.articlelistingpage",  # 500 ISE
        "great_international.baseinternationalsectorpage",  # 400 not found
        "great_international.capitalinvestopportunitypage",  # timeout
    ]
if "staging" in DIRECTORY_CMS_API_CLIENT_BASE_URL:
    SKIPPED_PAGE_TYPES = [
        "export_readiness.articlelistingpage",  # 500 ISE
        "export_readiness.homepageold",  # 400
        "export_readiness.internationallandingpage",  # 400
        "export_readiness.euexitinternationalformpage",  # 400
        "great_international.internationalarticlepage",  # 500 ISE
        "great_international.internationalcampaignpage",  # 500 ISE
    ]
if "uat" in DIRECTORY_CMS_API_CLIENT_BASE_URL:
    SKIPPED_PAGE_TYPES = [
        "great_international.baseinternationalsectorpage",  # 400 not found
    ]

ALL_PAGE_TYPES = get_pages_types(skip=SKIPPED_PAGE_TYPES)

EXRED_PAGE_TYPES = [t for t in ALL_PAGE_TYPES if t.startswith("export_readiness.")]
INTERNATIONAL_PAGE_TYPES = [t for t in ALL_PAGE_TYPES if t.startswith("great_international.")]
COMPONENTS_PAGE_TYPES = [t for t in ALL_PAGE_TYPES if t.startswith("components.")]

EXRED_PAGES = get_pages_from_api(EXRED_PAGE_TYPES, use_async_client=False)
INTERNATIONAL_PAGES = get_pages_from_api(INTERNATIONAL_PAGE_TYPES, use_async_client=False)

ALL_PAGES = {}
ALL_PAGES.update(EXRED_PAGES)
ALL_PAGES.update(INTERNATIONAL_PAGES)


@pytest.mark.parametrize(
    "relative_url",
    [
        URLs.CMS_API_IMAGES.relative,
        URLs.CMS_API_DOCUMENTS.relative,
    ],
)
def test_wagtail_get_disabled_content_endpoints(relative_url):
    response = cms_api_client.get(relative_url)
    assert response.status_code == HTTP_404_NOT_FOUND, status_error(
        HTTP_404_NOT_FOUND, response
    )


def test_wagtail_get_pages():
    endpoint = URLs.CMS_API_PAGES.relative
    response = cms_api_client.get(endpoint)
    assert response.status_code == HTTP_200_OK, status_error(
        HTTP_200_OK, response
    )


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
    "application", [
        "Components",
        "Great Domestic pages",
        "Great International pages",
    ]
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
    "application", [
        "Components",
        "Great Domestic pages",
        "great.gov.uk international",
    ]
)
def test_wagtail_get_pages_per_application_on_stage(application):
    test_wagtail_get_pages_per_application_on_dev(application)


@pytest.mark.prod
@pytest.mark.parametrize(
    "application", [
        "Components",
        "great.gov.uk",
        "great.gov.uk international",
    ]
)
def test_wagtail_get_pages_per_application_on_prod(application):
    test_wagtail_get_pages_per_application_on_dev(application)


@pytest.mark.parametrize("url, page_id", find_published_urls(ALL_PAGES))
def test_all_published_english_pages_should_return_200(url, page_id, basic_auth):
    get_and_assert(url, HTTP_200_OK, auth=basic_auth, allow_redirects=True, page_id=page_id)


@pytest.mark.parametrize(
    "url, page_id", find_published_translated_urls(ALL_PAGES)
)
def test_published_translated_pages_should_return_200_new(url, page_id, basic_auth):
    get_and_assert(url, HTTP_200_OK, auth=basic_auth, allow_redirects=True, page_id=page_id)


@pytest.mark.parametrize("url, page_id", find_draft_urls(ALL_PAGES))
def test_drafts_of_translated_pages_should_return_200_new(url, page_id, basic_auth):
    get_and_assert(url, HTTP_200_OK, auth=basic_auth, page_id=page_id)


@retry(
    wait_fixed=5000,
    stop_max_attempt_number=2,
    retry_on_exception=retriable_error,
)
@pytest.mark.parametrize(
    "service_name, slug",
    [
        # Domestic pages
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
        (SERVICE_NAMES.EXPORT_READINESS, "advice"),
        (SERVICE_NAMES.EXPORT_READINESS, "home"),
        (SERVICE_NAMES.EXPORT_READINESS, "international"),
        (SERVICE_NAMES.EXPORT_READINESS, "eu-exit-news"),
        (SERVICE_NAMES.EXPORT_READINESS, "community"),
        (SERVICE_NAMES.EXPORT_READINESS, "verification-missing"),
        (SERVICE_NAMES.EXPORT_READINESS, "company-not-found"),
        (SERVICE_NAMES.EXPORT_READINESS, "markets"),

        # Invest pages
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "invest"),
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "about-dit"),
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "about-uk"),
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "capital-invest"),
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "eu-exit-international"),
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "how-to-setup-in-the-uk"),
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "industries"),
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "midlands-engine"),
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "news"),
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "opportunities"),
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "south-england"),
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "uk-open-business"),

        # FAS pages
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "trade"),
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "contact"),

        # Industry pages
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "advanced-manufacturing"),
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "aerospace"),
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "automotive"),
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "creative-industries"),
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "energy"),
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "financial-services"),
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "health-and-life-sciences"),
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "technology"),

        # Regional pages
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "north-england"),
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "northern-ireland"),
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "scotland"),
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "south-england"),
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "wales"),
    ],
)
def test_wagtail_get_page_by_slug(cms_client, service_name, slug):
    """Check - https://uktrade.atlassian.net/browse/CMS-412"""
    response = cms_client.lookup_by_slug(slug, service_name=service_name)
    assert response.status_code == HTTP_200_OK, status_error(
        HTTP_200_OK, response
    )
    assert response.json()["meta"]["slug"] == slug


@pytest.mark.skip(reason="See CMS-1841")
@pytest.mark.parametrize(
    "service_name, slug",
    [
        (SERVICE_NAMES.GREAT_INTERNATIONAL, "high-potential-opportunities"),
        (SERVICE_NAMES.EXPORT_READINESS, "export-readiness-site-policy-pages"),
        (SERVICE_NAMES.EXPORT_READINESS, "all-export-readiness-contact-pages"),
        (SERVICE_NAMES.EXPORT_READINESS, "campaigns"),
    ],
)
def test_wagtail_get_page_by_slug_dont_return_500_ise(cms_client, service_name, slug):
    response = cms_client.lookup_by_slug(slug, service_name=service_name)
    assert response.status_code == HTTP_200_OK, status_error(
        HTTP_200_OK, response
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
    assert response.status_code == HTTP_200_OK, status_error(
        HTTP_200_OK, response
    )
    assert response.json()["meta"]["slug"] == slug
