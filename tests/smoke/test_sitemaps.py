# -*- coding: utf-8 -*-
import pytest
from bs4 import BeautifulSoup
from rest_framework.status import HTTP_200_OK

import allure
from directory_tests_shared import URLs
from directory_tests_shared.settings import BASICAUTH_PASS, BASICAUTH_USER
from tests.smoke.cms_api_helpers import get_and_assert

pytestmark = [
    allure.suite("sitemap.xml"),
    allure.feature("sitemap.xml"),
    allure.description(
        "A service which handles our Top Level Domain should expose a valid sitemap.xml"
        " which enables various Search Engines/Web Crawlers (like Google) to discover "
        "what pages are present and which change frequently. This allows them to crawl "
        "our site accordingly"
    ),
]


@allure.step("Check if sitemap.xml is present")
def get_urls_from_sitemap(sitemap_url: str, *, ignore_404: bool = False) -> list:
    result = []
    try:
        response = get_and_assert(
            url=sitemap_url,
            status_code=HTTP_200_OK,
            auth=(BASICAUTH_USER, BASICAUTH_PASS),
        )
        xml_soup = BeautifulSoup(response.content, "xml")
        if xml_soup.find_all("loc"):
            result = [location.text for location in xml_soup.find_all("loc")]
    except AssertionError:
        if not ignore_404:
            pass
        else:
            raise
    return result


@pytest.mark.parametrize("url", [URLs.DOMESTIC_SITEMAP.absolute])
def test_if_sitemap_exist(url, basic_auth):
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)


@pytest.mark.parametrize("url", [URLs.DOMESTIC_SITEMAP.absolute])
def test_check_sitemap_schema_and_if_it_contains_urls(url, basic_auth):
    schema = "http://www.sitemaps.org/schemas/sitemap/0.9"
    response = get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)
    xml_soup = BeautifulSoup(markup=response.content, features="lxml")

    assert xml_soup.urlset["xmlns"] == schema

    sitemap_urls = [location.text for location in xml_soup.find_all("loc")]
    error = (
        f"Expected to find at least 1 URL location in {url} but found an empty "
        f"sitemap.xml"
    )
    assert sitemap_urls, error


@allure.issue("CMS-1699", "Domestic - sitemap.xml contains links it shouldn't")
@pytest.mark.skip(reason="see CMS-1699")
@pytest.mark.parametrize(
    "url",
    [URLs.DOMESTIC_SITEMAP.absolute],  # contains a self-reference. See bug CMS-1699
)
def test_sitemap_should_not_contain_reference_to_itself(url):
    sitemap_urls = get_urls_from_sitemap(url)
    error = f"{url} contains reference to itself!"
    assert url not in sitemap_urls, error


@allure.issue("CMS-1699", "Domestic - sitemap.xml contains links it shouldn't")
@pytest.mark.skip(reason="see CMS-1699")
@pytest.mark.parametrize(
    "url", [URLs.DOMESTIC_SITEMAP.absolute]  # contains a dupe. See bug CMS-1699
)
def test_sitemap_should_not_contain_duplicated_links(url):
    sitemap_urls = get_urls_from_sitemap(url)
    dupes = set([url for url in sitemap_urls if sitemap_urls.count(url) > 1])
    error = f"{url} contains duplicated URLs: {', '.join(dupes)}"
    assert not dupes, error


@allure.issue("CMS-1699", "sitemap.xml contains links it shouldn't")
@allure.issue(
    "CMS-1811", "500 ISE when visiting report a trade barrier success page directly"
)
@pytest.mark.skip(reason="see CMS-1699 & CMS-1811")
@pytest.mark.parametrize(
    "url",
    set(get_urls_from_sitemap(URLs.DOMESTIC_SITEMAP.absolute, ignore_404=True))
    - {
        URLs.DOMESTIC_API_COMPANY_HOUSE_SEARCH.absolute,  # see CMS-1699
        URLs.TRADE_BARRIERS_REPORT_FORM_SUCCESS.absolute,  # see CMS-1811
    },
)
def test_check_all_urls_from_sitemap(url, basic_auth):
    get_and_assert(
        url=url, status_code=HTTP_200_OK, allow_redirects=True, auth=basic_auth
    )
