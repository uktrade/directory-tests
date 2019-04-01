import pytest
from rest_framework.status import HTTP_200_OK, HTTP_301_MOVED_PERMANENTLY

from tests import get_absolute_url
from tests.smoke.cms_api_helpers import get_and_assert


@pytest.mark.parametrize(
    "url",
    [
        get_absolute_url("ui-soo:landing"),
        get_absolute_url("ui-soo:search-results"),
    ],
)
def test_access_soo_endpoints(url, basic_auth):
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)


@pytest.mark.parametrize("url", [get_absolute_url("ui-soo:search-results")])
def test_access_soo_endpoints_without_trailing_slash(url, basic_auth):
    # get rid of trailing slash
    if url.endswith("/"):
        url = url[:-1]
    get_and_assert(
        url=url, status_code=HTTP_301_MOVED_PERMANENTLY, auth=basic_auth
    )


@pytest.mark.parametrize(
    "categories, countries",
    [
        ([""], "Japan"),
        (["Clothing & Accessories"], "France"),
        (["Clothing & Accessories", "Home & Garden"], ["France", "China"]),
    ],
)
def test_search_works(categories, countries, basic_auth):
    url = get_absolute_url("ui-soo:search-results")
    params = {
        "product_categories": categories,
        "operating_countries": countries,
    }
    get_and_assert(
        url=url,
        params=params,
        allow_redirects=True,
        status_code=HTTP_200_OK,
        auth=basic_auth,
    )


@pytest.mark.dev
@pytest.mark.parametrize(
    "market",
    [
        "1688com",
        "amazon-canada",
        "amazon-china",
        "amazon-france",
        "amazon-germany",
        "amazon-italy",
        "amazon-japan",
        "amazon-spain",
        "amazon-usa",
        "cdiscount",
        "ebay",
        "etsy",
        "flipkart",
        "jd-worldwide",
        "kaola",
        "newegg-inc",
        "privalia",
        "rakuten",
        "royal-mail-t-mall",
        "sfbest",
        "shangpin",
        "spartoo",
        "trademe",
    ],
)
def test_get_market_details_dev(market, basic_auth):
    url = get_absolute_url("ui-soo:market-details")
    absolute_url = f"{url}{market}"
    get_and_assert(
        url=absolute_url,
        allow_redirects=True,
        status_code=HTTP_200_OK,
        auth=basic_auth,
    )


@pytest.mark.stage
@pytest.mark.parametrize(
    "market",
    [
        "amazon-china",
        "amazon-france",
        "amazon-germany",
        "amazon-italy",
        "amazon-japan",
        "amazon-mexico",
        "amazon-spain",
        "amazon-usa",
        "cdiscount",
        "ebay",
        "flipkart",
        "fruugo",
        "goxip",
        "jd-worldwide",
        "kaola",
        "la-redoute",
        "linio",
        "newegg-business",
        "newegg-canada",
        "newegg-inc",
        "privalia",
        "rakuten",
        "royal-mail-t-mall",
        "sfbest",
        "shangpin",
        "spartoo",
        "trademe",
        "tthigo",
    ],
)
def test_get_market_details_stage(market, basic_auth):
    url = get_absolute_url("ui-soo:market-details")
    absolute_url = f"{url}{market}"
    get_and_assert(
        url=absolute_url,
        allow_redirects=True,
        status_code=HTTP_200_OK,
        auth=basic_auth,
    )


# test all market pages on Production
@pytest.mark.prod
@pytest.mark.parametrize(
    "market",
    [
        "1688com",
        "amazon-canada",
        "amazon-china",
        "amazon-france",
        "amazon-germany",
        "amazon-italy",
        "amazon-japan",
        "amazon-mexico",
        "amazon-spain",
        "amazon-usa",
        "bol",
        "catch",
        "cdiscount",
        "darty",
        "ebay",
        "eprice",
        "flipkart",
        "fnac",
        "fruugo",
        "goxip",
        "jd-worldwide",
        "kaola",
        "la-redoute",
        "linio",
        "mano-mano",
        "newegg-business",
        "newegg-canada",
        "newegg-inc",
        "onbuy",
        "privalia",
        "rakuten",
        "royal-mail-t-mall",
        "sfbest",
        "shangpin",
        "spartoo",
        "trademe",
        "tthigo",
    ],
)
def test_get_market_details_prod(market, basic_auth):
    url = get_absolute_url("ui-soo:market-details")
    absolute_url = f"{url}{market}"
    get_and_assert(
        url=absolute_url,
        allow_redirects=True,
        status_code=HTTP_200_OK,
        auth=basic_auth,
    )
