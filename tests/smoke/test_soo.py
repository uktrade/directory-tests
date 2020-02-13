# -*- coding: utf-8 -*-
import pytest
from rest_framework.status import HTTP_200_OK, HTTP_301_MOVED_PERMANENTLY

import allure
from directory_tests_shared import URLs
from directory_tests_shared.settings import BASICAUTH_PASS, BASICAUTH_USER
from directory_tests_shared.utils import extract_attributes_by_css, extract_by_css
from tests.smoke.cms_api_helpers import get_and_assert

pytestmark = [
    allure.suite("Selling Online Overseas"),
    allure.feature("Selling Online Overseas"),
]


@allure.step("Get slugs for all marketplaces")
def get_all_market_slugs(*, auth: tuple = (BASICAUTH_USER, BASICAUTH_PASS)) -> list:
    start_page = f"{URLs.SOO_SEARCH_RESULTS.absolute}?category_id=&country_id=&commit="
    response = get_and_assert(url=start_page, status_code=HTTP_200_OK, auth=auth)
    content = response.content.decode("UTF-8")
    hrefs = extract_attributes_by_css(
        content, "a.market-header-link", attrs=["href"], text=False
    )

    last_page_number = int(
        extract_by_css(content, "nav.pagination > ol > li:last-of-type > a::text")
    )
    if last_page_number > 1:
        for page_number in range(2, last_page_number + 1):
            url = f"{start_page}&page={page_number}"
            response = get_and_assert(url=url, status_code=HTTP_200_OK, auth=auth)
            content = response.content.decode("UTF-8")
            hrefs += extract_attributes_by_css(
                content, "a.market-header-link", attrs=["href"], text=False
            )
    # flatten the results and return only the market's slug value e.g. tthigo
    # results format is:
    # [{'href': '/selling-online-overseas/markets/details/tthigo/'}, ...]
    slugs = [href["href"].split("/")[-2] for href in hrefs]
    return slugs


@pytest.mark.parametrize(
    "url", [URLs.SOO_LANDING.absolute, URLs.SOO_SEARCH_RESULTS.absolute]
)
def test_access_soo_endpoints(url, basic_auth):
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)


@pytest.mark.parametrize("url", [URLs.SOO_SEARCH_RESULTS.absolute])
def test_access_soo_endpoints_without_trailing_slash(url, basic_auth):
    # get rid of trailing slash
    if url.endswith("/"):
        url = url[:-1]
    get_and_assert(url=url, status_code=HTTP_301_MOVED_PERMANENTLY, auth=basic_auth)


@pytest.mark.parametrize(
    "categories, countries",
    [
        ([""], "Japan"),
        (["Clothing & Accessories"], "France"),
        (["Clothing & Accessories", "Home & Garden"], ["France", "China"]),
    ],
)
def test_search_works(categories, countries, basic_auth):
    url = URLs.SOO_SEARCH_RESULTS.absolute
    params = {"product_categories": categories, "operating_countries": countries}
    get_and_assert(
        url=url,
        params=params,
        allow_redirects=True,
        status_code=HTTP_200_OK,
        auth=basic_auth,
    )


@pytest.mark.parametrize(
    "url",
    list(
        map(
            lambda name: URLs.SOO_MARKET_DETAILS.absolute_template.format(market=name),
            get_all_market_slugs(),
        )
    ),
)
def test_get_market_details(url, basic_auth):
    get_and_assert(
        url=url, allow_redirects=True, status_code=HTTP_200_OK, auth=basic_auth
    )
