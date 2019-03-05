import pytest
import requests
from rest_framework.status import *

from tests import get_absolute_url
from tests.smoke.cms_api_helpers import status_error


@pytest.mark.parametrize("absolute_url", [
    get_absolute_url("ui-soo:landing"),
    get_absolute_url("ui-soo:search-results"),
])
def test_access_soo_endpoints(absolute_url):
    response = requests.get(absolute_url, allow_redirects=True)
    assert response.status_code == HTTP_200_OK, status_error(
        HTTP_200_OK, response
    )


@pytest.mark.parametrize("absolute_url", [
    get_absolute_url("ui-soo:search-results"),
])
def test_access_soo_endpoints_without_trailing_slash(
        absolute_url):
    # get rid of trailing slash
    absolute_url = absolute_url[:-1]
    response = requests.get(absolute_url, allow_redirects=False)
    assert response.status_code == HTTP_301_MOVED_PERMANENTLY, status_error(
        HTTP_301_MOVED_PERMANENTLY, response
    )


@pytest.mark.parametrize("categories, countries", [
    ([""], "Japan"),
    (["Clothing & Accessories"], "France"),
    (["Clothing & Accessories", "Home & Garden"], ["France", "China"]),
])
def test_search_works(categories, countries):
    url = get_absolute_url("ui-soo:search-results")
    params = {
        "product_categories": categories,
        "operating_countries": countries
    }
    response = requests.get(url, params=params, allow_redirects=True)
    assert response.status_code == HTTP_200_OK, status_error(
        HTTP_200_OK, response
    )


@pytest.mark.dev
@pytest.mark.parametrize("market", [
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
])
def test_get_market_details_dev(market):
    url = get_absolute_url("ui-soo:market-details")
    absolute_url = f"{url}{market}"
    response = requests.get(absolute_url, allow_redirects=True)
    assert response.status_code == HTTP_200_OK, status_error(
        HTTP_200_OK, response
    )


@pytest.mark.stage
@pytest.mark.parametrize("market", [
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
])
def test_get_market_details_stage(market):
    url = get_absolute_url("ui-soo:market-details")
    absolute_url = f"{url}{market}"
    response = requests.get(absolute_url, allow_redirects=True)
    assert response.status_code == HTTP_200_OK, status_error(
        HTTP_200_OK, response
    )


# test all market pages on Production
@pytest.mark.prod
@pytest.mark.parametrize("market", [
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
])
def test_get_market_details_prod(market):
    url = get_absolute_url("ui-soo:market-details")
    absolute_url = f"{url}{market}"
    response = requests.get(absolute_url, allow_redirects=True)
    assert response.status_code == HTTP_200_OK, status_error(
        HTTP_200_OK, response
    )
