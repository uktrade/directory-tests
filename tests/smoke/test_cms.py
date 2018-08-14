import http.client
from pprint import pformat

import pytest
import requests
from directory_cms_client.client import cms_api_client
from requests import Response

from tests import get_absolute_url, get_relative_url
from tests.settings import DIRECTORY_API_HEALTH_CHECK_TOKEN as TOKEN


def status_error(expected_status_code: int, response: Response):
    return (
        f"{response.request.method} {response.url} returned "
        f"{response.status_code} instead of expected "
        f"{expected_status_code}"
    )


def test_healthcheck_ping_endpoint():
    endpoint = get_relative_url("cms-healthcheck:ping")
    response = cms_api_client.get(
        url=endpoint, language_code=None, draft_token=None
    )
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
    response = cms_api_client.get(
        url=relative_url, language_code=None, draft_token=None
    )
    assert response.status_code == http.client.NOT_FOUND, status_error(
        http.client.NOT_FOUND, response
    )


def test_wagtail_get_pages():
    response = cms_api_client.get(
        url=get_relative_url("cms-api:pages"),
        language_code=None,
        draft_token=None,
    )
    assert response.status_code == http.client.OK, status_error(
        http.client.OK, response
    )


@pytest.mark.parametrize(
    "slug",
    [
        "landing-page",
        "industry-contact",
        "industries-landing-page",
        "get-finance",
        "terms-and-conditions",
        "privacy-and-cookies",
        "legal-services",
    ],
)
def test_wagtail_get_page_by_slug(slug):
    relative_url = get_relative_url("cms-api:pages-by-slug").format(slug)
    response = cms_api_client.get(
        url=relative_url, language_code=None, draft_token=None
    )
    assert response.status_code == http.client.OK, status_error(
        http.client.OK, response
    )
    assert response.json()["meta"]["slug"] == slug


@pytest.mark.parametrize("limit", [2, 10, 20])
def test_wagtail_get_number_of_pages(limit):
    query = "?order=id&limit={}".format(limit)
    relative_url = get_relative_url("cms-api:pages") + query
    response = cms_api_client.get(
        url=relative_url, language_code=None, draft_token=None
    )
    assert len(response.json()["items"]) == limit


def test_wagtail_can_list_only_20_pages():
    query = "?limit=21"
    relative_url = get_relative_url("cms-api:pages") + query
    response = cms_api_client.get(
        url=relative_url, language_code=None, draft_token=None
    )
    assert response.json()["message"] == "limit cannot be higher than 20"


@pytest.mark.parametrize(
    "application", ["Export Readiness pages", "Find a Supplier Pages"]
)
def test_wagtail_get_pages_per_application(application):
    # Get ID of specific application (parent page)
    query = "?title={}".format(application)
    relative_url = get_relative_url("cms-api:pages") + query
    response = cms_api_client.get(
        url=relative_url, language_code=None, draft_token=None
    )
    assert response.json()["meta"]["total_count"] == 1
    application_id = response.json()["items"][0]["id"]

    # Get inf about its child pages
    query = "?child_of={}".format(application_id)
    relative_url = get_relative_url("cms-api:pages") + query
    response = cms_api_client.get(
        url=relative_url, language_code=None, draft_token=None
    )
    assert response.json()["meta"]["total_count"] > 0


def get_page_ids_by_type(page_type):
    page_ids = []

    # get first page of results
    url = "{}?type={}".format(get_relative_url("cms-api:pages"), page_type)
    response = cms_api_client.get(
        url=url, language_code=None, draft_token=None
    )
    assert response.status_code == http.client.OK, status_error(
        http.client.OK, response
    )

    # get IDs of all pages from the response
    content = response.json()
    page_ids += [page["id"] for page in content["items"]]

    total_count = content["meta"]["total_count"]
    while len(page_ids) < total_count:
        offset = len(content["items"])
        url = "{}?type={}&offset={}".format(
            get_relative_url("cms-api:pages"), page_type, offset
        )
        response = cms_api_client.get(
            url=url, language_code=None, draft_token=None
        )
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
        "export_readiness.PrivacyAndCookiesPage",
        "export_readiness.TermsAndConditionsPage",
        "find_a_supplier.IndustryArticlePage",
        "find_a_supplier.IndustryContactPage",
        "find_a_supplier.IndustryLandingPage",
        "find_a_supplier.IndustryPage",
        "find_a_supplier.LandingPage",
        "invest.InfoPage",
        "invest.InvestHomePage",
        # "invest.RegionLandingPage",
        "invest.SectorLandingPage",
        # "invest.SectorPage",
        # "invest.SetupGuideLandingPage",
        # "invest.SetupGuidePage",
    ],
)
def test_all_published_pages_should_return_200(page_type):
    results = []
    page_ids = get_page_ids_by_type(page_type)
    for page_id in page_ids:
        url = "{}{}/".format(get_relative_url("cms-api:pages"), page_id)
        try:
            api_response = cms_api_client.get(
                url=url, language_code=None, draft_token=None
            )
        except Exception as ex:
            results.append((page_id, url, str(ex)))
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
            print("{} returned {}".format(url, api_response.status_code))
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
        "export_readiness.GetFinancePage",
        "export_readiness.PrivacyAndCookiesPage",
        "export_readiness.TermsAndConditionsPage",
        "find_a_supplier.IndustryArticlePage",
        "find_a_supplier.IndustryContactPage",
        "find_a_supplier.IndustryLandingPage",
        "find_a_supplier.IndustryPage",
        "find_a_supplier.LandingPage",
        "invest.InfoPage",
        "invest.InvestHomePage",
        # "invest.RegionLandingPage",
        "invest.SectorLandingPage",
        # "invest.SectorPage",
        # "invest.SetupGuidePage",
        # "invest.SetupGuideLandingPage",
    ],
)
def test_published_translated_pages_should_return_200(page_type):
    results = []
    page_ids = get_page_ids_by_type(page_type)
    for page_id in page_ids:
        url = "{}{}/".format(get_relative_url("cms-api:pages"), page_id)
        try:
            api_response = cms_api_client.get(
                url=url, language_code=None, draft_token=None
            )
        except Exception as ex:
            results.append((page_id, url, str(ex)))
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
            print("{} returned {}".format(url, api_response.status_code))
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
        "export_readiness.GetFinancePage",
        "export_readiness.PrivacyAndCookiesPage",
        "export_readiness.TermsAndConditionsPage",
        "find_a_supplier.IndustryArticlePage",
        "find_a_supplier.IndustryContactPage",
        "find_a_supplier.IndustryLandingPage",
        "find_a_supplier.IndustryPage",
        "find_a_supplier.LandingPage",
        "invest.InfoPage",
        "invest.InvestHomePage",
        # "invest.RegionLandingPage",
        "invest.SectorLandingPage",
        # "invest.SectorPage",
        # "invest.SetupGuideLandingPage",
        "invest.SetupGuidePage",
    ],
)
def test_draft_pages_should_return_200(page_type):
    results = []
    page_ids = get_page_ids_by_type(page_type)
    for page_id in page_ids:
        url = "{}{}/".format(get_relative_url("cms-api:pages"), page_id)
        try:
            api_response = cms_api_client.get(
                url=url, language_code=None, draft_token=None
            )
        except Exception as ex:
            results.append((page_id, url, str(ex)))
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
            print("{} returned {}".format(url, api_response.status_code))
    non_200 = [result for result in results if result[2] != 200]
    template = "Page ID: {} URL: {} Status Code: {}"
    formatted_non_200 = [template.format(*result) for result in non_200]
    error_msg = "{} out of {} published pages of type {} are broken {}".format(
        len(non_200), len(results), page_type, pformat(formatted_non_200)
    )
    assert not non_200, error_msg
