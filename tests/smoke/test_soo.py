import pytest
from rest_framework.status import HTTP_200_OK, HTTP_301_MOVED_PERMANENTLY

from tests import URLs
from tests.smoke.cms_api_helpers import get_and_assert


@pytest.mark.parametrize(
    "url",
    [
        URLs.SOO_LANDING.absolute,
        URLs.SOO_SEARCH_RESULTS.absolute,
    ],
)
def test_access_soo_endpoints(url, basic_auth):
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)


@pytest.mark.parametrize("url", [URLs.SOO_SEARCH_RESULTS.absolute])
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
    url = URLs.SOO_SEARCH_RESULTS.absolute
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
    "url",
    list(
        map(
            lambda name: URLs.SOO_MARKET_DETAILS.absolute_template.format(market=name),
            [
                "1688com",
                "alibaba-direct",
                "allegro",
                "amazon-canada",
                "amazon-china",
                "amazon-france",
                "amazon-germany",
                "amazon-india",
                "amazon-italy",
                "amazon-japan",
                "amazon-spain",
                "amazon-usa",
                "cdiscount",
                "ctrip",
                "ebay",
                "etsy",
                "flipkart",
                "jack-russell-emporium-on-jdcom",
                "jd-worldwide",
                "kaola",
                "newegg-inc",
                "otto",
                "privalia",
                "rakuten",
                "royal-mail-t-mall",
                "sfbest",
                "shangpin",
                "spartoo",
                "the-iconic",
                "tmall-global",
                "trademe",
                "vip-shop",
                "westwing",
                "xiu",
                "zalora",
            ]
        )
    ),
)
def test_get_market_details_dev(url, basic_auth):
    get_and_assert(
        url=url,
        allow_redirects=True,
        status_code=HTTP_200_OK,
        auth=basic_auth,
    )


@pytest.mark.stage
@pytest.mark.parametrize(
    "url",
    list(
        map(
            lambda name: URLs.SOO_MARKET_DETAILS.absolute_template.format(market=name),
            [
                "allegro",
                "amazon-china",
                "amazon-france",
                "amazon-germany",
                "amazon-india",
                "amazon-italy",
                "amazon-japan",
                "amazon-mexico",
                "amazon-spain",
                "amazon-usa",
                "cdiscount",
                "ctrip",
                "dafiti",
                "ebay",
                "etsy",
                "flipkart",
                "fruugo",
                "goxip",
                "jd-worldwide",
                "kaola",
                "la-redoute",
                "lamoda",
                "linio",
                "mercado-libre",
                "newegg-business",
                "newegg-canada",
                "newegg-inc",
                "otto",
                "privalia",
                "rakuten",
                "royal-mail-t-mall",
                "sfbest",
                "shangpin",
                "spartoo",
                "the-iconic",
                "tmall-global",
                "tthigo",
                "westwing",
                "xiu",
                "zalora",
            ]
        )
    ),
)
def test_get_market_details_stage(url, basic_auth):
    get_and_assert(
        url=url,
        allow_redirects=True,
        status_code=HTTP_200_OK,
        auth=basic_auth,
    )


# test all market pages on Production
@pytest.mark.prod
@pytest.mark.parametrize(
    "url",
    list(
        map(
            lambda name: URLs.SOO_MARKET_DETAILS.absolute_template.format(market=name),
            [
                "1688com",
                "amazon-australia",
                "amazon-canada",
                "amazon-france",
                "amazon-germany",
                "amazon-italy",
                "amazon-japan",
                "amazon-mexico",
                "amazon-spain",
                "amazon-usa",
                "amazon-uae",
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
                "realde",
                "royal-mail-t-mall",
                "spartoo",
                "trademe",
                "themarket",
                "tthigo",
            ]
        )
    ),
)
def test_get_market_details_prod(url, basic_auth):
    get_and_assert(
        url=url,
        allow_redirects=True,
        status_code=HTTP_200_OK,
        auth=basic_auth,
    )
