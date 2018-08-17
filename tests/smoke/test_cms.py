import asyncio
import http.client
from pprint import pformat

import pytest
import requests
from directory_cms_client.client import cms_api_client
from directory_cms_client.helpers import AbstractCMSResponse
from directory_cms_client.client import DirectoryCMSClient
from directory_constants.constants import cms as SERVICE_NAMES
from urllib.parse import urlparse

from tests import get_absolute_url, get_relative_url
from tests.settings import (
    DIRECTORY_API_HEALTH_CHECK_TOKEN as TOKEN,
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
        service_name=SERVICE_NAMES.INVEST,
    )


async def fetch(endpoints):
    async_loop = asyncio.get_event_loop()
    async with async_cms_client() as client:
        futures = [
            async_loop.run_in_executor(
                None,
                client.get,
                endpoint
            )
            for endpoint in endpoints
        ]
        return await asyncio.gather(*futures)


def status_error(expected_status_code: int, response: AbstractCMSResponse):
    return (
        f"{response.raw_response.request.method} {response.raw_response.url} "
        f"returned {response.status_code} instead of expected "
        f"{expected_status_code}\n"
        f"REQ headers: {pformat(response.raw_response.request.headers)}\n"
        f"RSP headers: {pformat(response.raw_response.headers)}"
    )


def test_healthcheck_ping_endpoint():
    endpoint = get_relative_url("cms-healthcheck:ping")
    response = cms_api_client.get(endpoint)
    assert response.status_code == http.client.OK, status_error(
        http.client.OK, response
    )


@pytest.mark.skip(reason="check ticket: CMS-146")
def test_healthcheck_database_endpoint():
    params = {"token": TOKEN}
    absolute_url = get_absolute_url("cms-healthcheck:database")
    response = requests.get(absolute_url, params=params)
    error_msg = "Expected 200 but got {}\n{}".format(
        response.status_code, response.content.decode("utf-8")
    )
    assert response.status_code == http.client.OK, error_msg


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


@pytest.mark.parametrize(
    "service_name, slug",
    [
        (SERVICE_NAMES.EXPORT_READINESS, "get-finance"),
        (SERVICE_NAMES.EXPORT_READINESS, "terms-and-conditions"),
        (SERVICE_NAMES.EXPORT_READINESS, "privacy-and-cookies"),
        (SERVICE_NAMES.EXPORT_READINESS, "performance-dashboard"),
        (SERVICE_NAMES.EXPORT_READINESS, "performance-dashboard-notes"),
        (SERVICE_NAMES.EXPORT_READINESS, "performance-dashboard-invest"),
        (SERVICE_NAMES.EXPORT_READINESS, "performance-dashboard-trade-profiles"),
        (SERVICE_NAMES.EXPORT_READINESS, "performance-dashboard-selling-online-overseas"),
        (SERVICE_NAMES.EXPORT_READINESS, "performance-dashboard-export-opportunities"),

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
        (SERVICE_NAMES.INVEST, "energy-from-waste"),
        (SERVICE_NAMES.INVEST, "financial-services"),
        (SERVICE_NAMES.INVEST, "financial-technology"),
        (SERVICE_NAMES.INVEST, "food-and-drink"),
        (SERVICE_NAMES.INVEST, "food-service-and-catering"),
        (SERVICE_NAMES.INVEST, "free-from-foods"),
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
        (SERVICE_NAMES.INVEST, "south-of-england"),
        (SERVICE_NAMES.INVEST, "wales"),

        (SERVICE_NAMES.INVEST, "setup-guide-landing-page"),
        (SERVICE_NAMES.INVEST, "apply-for-a-uk-visa"),
        (SERVICE_NAMES.INVEST, "establish-a-base-for-business-in-the-uk"),
        (SERVICE_NAMES.INVEST, "hire-skilled-workers-for-your-uk-operations"),
        (SERVICE_NAMES.INVEST, "open-a-uk-business-bank-account"),
        (SERVICE_NAMES.INVEST, "set-up-a-company-in-the-uk"),
        (SERVICE_NAMES.INVEST, "understand-uk-tax-and-incentives"),
    ],
)
def test_wagtail_get_page_by_slug(cms_client, service_name, slug):
    """Check - https://uktrade.atlassian.net/browse/CMS-412"""
    cms_client.service_name = service_name
    response = cms_client.lookup_by_slug(slug)
    assert response.status_code == http.client.OK, status_error(
        http.client.OK, response
    )
    assert response.json()["meta"]["slug"] == slug


@pytest.mark.parametrize(
    "service_name, prefix, slug",
    [
        (SERVICE_NAMES.INVEST, "invest-", "home-page"),

        (SERVICE_NAMES.INVEST, "invest-", "sector-landing-page"),
        (SERVICE_NAMES.INVEST, "invest-", "advanced-manufacturing"),
        (SERVICE_NAMES.INVEST, "invest-", "aerospace"),
        (SERVICE_NAMES.INVEST, "invest-", "agri-tech"),
        (SERVICE_NAMES.INVEST, "invest-", "asset-management"),
        (SERVICE_NAMES.INVEST, "invest-", "automotive"),
        (SERVICE_NAMES.INVEST, "invest-", "automotive-research-and-development"),
        (SERVICE_NAMES.INVEST, "invest-", "automotive-supply-chain"),
        (SERVICE_NAMES.INVEST, "invest-", "capital-investment"),
        (SERVICE_NAMES.INVEST, "invest-", "chemicals"),
        (SERVICE_NAMES.INVEST, "invest-", "creative-content-and-production"),
        (SERVICE_NAMES.INVEST, "invest-", "creative-industries"),
        (SERVICE_NAMES.INVEST, "invest-", "data-analytics"),
        (SERVICE_NAMES.INVEST, "invest-", "digital-media"),
        (SERVICE_NAMES.INVEST, "invest-", "electrical-networks"),
        (SERVICE_NAMES.INVEST, "invest-", "energy"),
        (SERVICE_NAMES.INVEST, "invest-", "energy-from-waste"),
        (SERVICE_NAMES.INVEST, "invest-", "financial-services"),
        (SERVICE_NAMES.INVEST, "invest-", "financial-technology"),
        (SERVICE_NAMES.INVEST, "invest-", "food-and-drink"),
        (SERVICE_NAMES.INVEST, "invest-", "food-service-and-catering"),
        (SERVICE_NAMES.INVEST, "invest-", "free-from-foods"),
        (SERVICE_NAMES.INVEST, "invest-", "health-and-life-sciences"),
        (SERVICE_NAMES.INVEST, "invest-", "meat-poultry-and-dairy"),
        (SERVICE_NAMES.INVEST, "invest-", "medical-technology"),
        (SERVICE_NAMES.INVEST, "invest-", "motorsport"),
        (SERVICE_NAMES.INVEST, "invest-", "nuclear-energy"),
        (SERVICE_NAMES.INVEST, "invest-", "offshore-wind-energy"),
        (SERVICE_NAMES.INVEST, "invest-", "oil-and-gas"),
        (SERVICE_NAMES.INVEST, "invest-", "pharmaceutical-manufacturing"),
        (SERVICE_NAMES.INVEST, "invest-", "retail"),
        (SERVICE_NAMES.INVEST, "invest-", "technology"),

        (SERVICE_NAMES.INVEST, "invest-", "uk-region-landing-page"),
        (SERVICE_NAMES.INVEST, "invest-", "london"),
        (SERVICE_NAMES.INVEST, "invest-", "north-england"),
        (SERVICE_NAMES.INVEST, "invest-", "northern-ireland"),
        (SERVICE_NAMES.INVEST, "invest-", "scotland"),
        (SERVICE_NAMES.INVEST, "invest-", "south-of-england"),
        (SERVICE_NAMES.INVEST, "invest-", "wales"),

        (SERVICE_NAMES.INVEST, "invest-", "setup-guide-landing-page"),
        (SERVICE_NAMES.INVEST, "invest-", "apply-for-a-uk-visa"),
        (SERVICE_NAMES.INVEST, "invest-", "establish-a-base-for-business-in-the-uk"),
        (SERVICE_NAMES.INVEST, "invest-", "hire-skilled-workers-for-your-uk-operations"),
        (SERVICE_NAMES.INVEST, "invest-", "open-a-uk-business-bank-account"),
        (SERVICE_NAMES.INVEST, "invest-", "set-up-a-company-in-the-uk"),
        (SERVICE_NAMES.INVEST, "invest-", "understand-uk-tax-and-incentives"),
    ],
)
def test_wagtail_get_page_by_historic_slug_with_service_prefix(cms_client, service_name, prefix, slug):
    cms_client.service_name = service_name
    response = cms_client.lookup_by_slug(prefix + slug)
    assert response.status_code == http.client.OK, status_error(
        http.client.OK, response
    )
    assert response.json()["meta"]["slug"] == slug


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
    "application", ["Export Readiness pages", "Find a Supplier Pages"]
)
def test_wagtail_get_pages_per_application(application):
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


def get_page_ids_by_type(page_type):
    page_ids = []

    # get first page of results
    endpoint = "{}?type={}".format(get_relative_url("cms-api:pages"), page_type)
    response = cms_api_client.get(endpoint)
    assert response.status_code == http.client.OK, status_error(
        http.client.OK, response
    )

    # get IDs of all pages from the response
    content = response.json()
    page_ids += [page["id"] for page in content["items"]]

    total_count = content["meta"]["total_count"]
    while len(page_ids) < total_count:
        offset = len(content["items"])
        endpoint = "{}?type={}&offset={}".format(
            get_relative_url("cms-api:pages"), page_type, offset
        )
        response = cms_api_client.get(endpoint)
        assert response.status_code == http.client.OK, status_error(
            http.client.OK, response
        )
        content = response.json()
        page_ids += [page["id"] for page in content["items"]]

    assert len(list(sorted(page_ids))) == total_count
    return page_ids


@pytest.mark.parametrize(
    "page_type",
    [
        "export_readiness.GetFinancePage",
        "export_readiness.PerformanceDashboardNotesPage",
        "export_readiness.PrivacyAndCookiesPage",
        "export_readiness.TermsAndConditionsPage",
        "find_a_supplier.IndustryArticlePage",
        "find_a_supplier.IndustryContactPage",
        "find_a_supplier.IndustryLandingPage",
        "find_a_supplier.IndustryPage",
        "find_a_supplier.LandingPage",
        "invest.InfoPage",
        "invest.InvestHomePage",
        "invest.SectorLandingPage",
    ],
)
def test_all_published_pages_should_return_200(page_type):
    results = []
    page_ids = get_page_ids_by_type(page_type)
    for page_id in page_ids:
        endpoint = "{}{}/".format(get_relative_url("cms-api:pages"), page_id)
        try:
            api_response = cms_api_client.get(endpoint)
        except Exception as ex:
            results.append((page_id, endpoint, str(ex)))
            continue
        if api_response.status_code == 200:
            live_url = api_response.json()["meta"]["url"]
            try:
                live_response = requests.get(live_url)
            except Exception as ex:
                results.append((page_id, live_url, str(ex)))
                continue
            results.append((page_id, live_url, live_response.status_code))
        else:
            print("{} returned {}".format(endpoint, api_response.status_code))
    non_200 = [result for result in results if result[2] != 200]
    template = "Page ID: {} URL: {} Status Code: {}"
    formatted_non_200 = [template.format(*result) for result in non_200]
    error_msg = "{} out of {} published pages of type {} are broken {}".format(
        len(non_200), len(results), page_type, pformat(formatted_non_200)
    )
    assert not non_200, error_msg


@pytest.mark.skip(reason="check ticket: CMS-413")
@pytest.mark.parametrize(
    "page_type",
    [
        "export_readiness.PerformanceDashboardPage",
        "invest.RegionLandingPage",
        "invest.SectorPage",
        "invest.SetupGuideLandingPage",
        "invest.SetupGuidePage",
    ],
)
def test_all_published_pages_should_return_200_failing_examples(page_type):
    test_all_published_pages_should_return_200(page_type)


@pytest.mark.parametrize(
    "page_type",
    [
        "export_readiness.GetFinancePage",
        "export_readiness.PerformanceDashboardNotesPage",
        "export_readiness.PrivacyAndCookiesPage",
        "export_readiness.TermsAndConditionsPage",
        "find_a_supplier.IndustryArticlePage",
        "find_a_supplier.IndustryContactPage",
        "find_a_supplier.IndustryLandingPage",
        "find_a_supplier.IndustryPage",
        "find_a_supplier.LandingPage",
    ],
)
def test_published_translated_pages_should_return_200(page_type):
    results = []
    page_ids = get_page_ids_by_type(page_type)
    for page_id in page_ids:
        endpoint = "{}{}/".format(get_relative_url("cms-api:pages"), page_id)
        try:
            api_response = cms_api_client.get(endpoint)
        except Exception as ex:
            results.append((page_id, endpoint, str(ex)))
            continue
        if api_response.status_code == 200:
            page = api_response.json()
            live_url = page["meta"]["url"]
            lang_codes = [lang[0] for lang in page["meta"]["languages"]]
            for code in lang_codes:
                lang_url = "{}?lang={}".format(live_url, code)
                try:
                    live_response = requests.get(lang_url)
                except Exception as ex:
                    results.append((page_id, lang_url, str(ex)))
                    continue
                results.append((page_id, lang_url, live_response.status_code))
        else:
            print("{} returned {}".format(endpoint, api_response.status_code))
    non_200 = [result for result in results if result[2] != 200]
    template = "Page ID: {} URL: {} Status Code: {}"
    formatted_non_200 = [template.format(*result) for result in non_200]
    error_msg = "{} out of {} published pages of type {} are broken {}".format(
        len(non_200), len(results), page_type, pformat(formatted_non_200)
    )
    assert not non_200, error_msg


@pytest.mark.parametrize(
    "page_type",
    [
        "invest.SectorPage",
        "invest.InfoPage",
        "invest.InvestHomePage",
        "invest.SectorLandingPage",
    ],
)
def test_published_translated_invest_pages_should_return_200_async(page_type):
    page_ids = get_page_ids_by_type(page_type)
    base = "https://dev.cms.directory.uktrade.io/api/pages/"
    api_endpoints = [f"{base}{page_id}/" for page_id in page_ids]

    loop = asyncio.get_event_loop()
    responses = loop.run_until_complete(fetch(api_endpoints))
    assert all(r.status_code == 200 for r in responses)

    lang_urls = []
    for response in responses:
        live_url = response.json()["meta"]["url"]
        parsed = urlparse(live_url)
        lang_codes = [lang[0] for lang in response.json()["meta"]["languages"]]
        for code in lang_codes:
            if code == "en-gb":
                url = live_url
                lang_urls.append(url)
            else:
                url = f"{parsed.scheme}://{parsed.netloc}/{code}{parsed.path}"
                lang_urls.append(url)

    loop = asyncio.get_event_loop()
    responses = loop.run_until_complete(fetch(lang_urls))
    failed = [r for r in responses if r.status_code != 200]
    msg = ", ".join([f"{r.raw_response.url} → {r.status_code}" for r in failed])
    assert all(r.status_code == 200 for r in responses), f"Failed URLs: {msg}"


@pytest.mark.skip(reason="check ticket: CMS-413")
@pytest.mark.parametrize(
    "page_type",
    [
        "export_readiness.PerformanceDashboardPage",
    ],
)
def test_published_translated_pages_should_return_200_failing_examples_cms413(page_type):
    test_published_translated_pages_should_return_200(page_type)


@pytest.mark.skip(reason="check ticket: CMS-414")
@pytest.mark.parametrize(
    "page_type",
    [
        "invest.RegionLandingPage",
    ],
)
def test_published_translated_pages_should_return_200_failing_examples_cms414(page_type):
    test_published_translated_pages_should_return_200(page_type)


@pytest.mark.skip(reason="check ticket: CMS-415")
@pytest.mark.parametrize(
    "page_type",
    [
        "invest.SectorPage",
    ],
)
def test_published_translated_pages_should_return_200_failing_examples_cms415(page_type):
    test_published_translated_pages_should_return_200(page_type)


@pytest.mark.skip(reason="check ticket: CMS-416")
@pytest.mark.parametrize(
    "page_type",
    [
        "invest.SetupGuidePage",
        "invest.SetupGuideLandingPage",
    ],
)
def test_published_translated_pages_should_return_200_failing_examples_cms416(page_type):
    test_published_translated_pages_should_return_200(page_type)


@pytest.mark.parametrize(
    "page_type",
    [
        "export_readiness.GetFinancePage",
        "export_readiness.PerformanceDashboardNotesPage",
        "export_readiness.PerformanceDashboardPage",
        "export_readiness.PrivacyAndCookiesPage",
        "export_readiness.TermsAndConditionsPage",
        "find_a_supplier.IndustryArticlePage",
        "find_a_supplier.IndustryContactPage",
        "find_a_supplier.IndustryLandingPage",
        "find_a_supplier.IndustryPage",
        "find_a_supplier.LandingPage",
        "invest.InfoPage",
        "invest.InvestHomePage",
        "invest.RegionLandingPage",
        "invest.SectorLandingPage",
        "invest.SectorPage",
        "invest.SetupGuideLandingPage",
        "invest.SetupGuidePage",
    ],
)
def test_draft_pages_should_return_200(page_type):
    results = []
    page_ids = get_page_ids_by_type(page_type)
    for page_id in page_ids:
        endpoint = "{}{}/".format(get_relative_url("cms-api:pages"), page_id)
        try:
            api_response = cms_api_client.get(endpoint)
        except Exception as ex:
            results.append((page_id, endpoint, str(ex)))
            continue
        if api_response.status_code == 200:
            page = api_response.json()
            draft_token = page["meta"]["draft_token"]
            if draft_token is not None:
                draft_url = "{}?draft_token={}".format(
                    page["meta"]["url"], draft_token
                )
                lang_codes = [lang[0] for lang in page["meta"]["languages"]]
                for code in lang_codes:
                    lang_url = "{}&lang={}".format(draft_url, code)
                    try:
                        draft_response = requests.get(lang_url)
                    except Exception as ex:
                        results.append((page_id, lang_url, str(ex)))
                        continue
                    results.append(
                        (page_id, lang_url, draft_response.status_code)
                    )
        else:
            print("{} returned {}".format(endpoint, api_response.status_code))
    non_200 = [result for result in results if result[2] != 200]
    template = "Page ID: {} URL: {} Status Code: {}"
    formatted_non_200 = [template.format(*result) for result in non_200]
    error_msg = "{} out of {} published pages of type {} are broken {}".format(
        len(non_200), len(results), page_type, pformat(formatted_non_200)
    )
    assert not non_200, error_msg
