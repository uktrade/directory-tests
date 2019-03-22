import pytest
from rest_framework.status import HTTP_200_OK, HTTP_302_FOUND

from tests import get_absolute_url
from tests.smoke.cms_api_helpers import get_and_assert


@pytest.mark.parametrize(
    "url",
    [
        get_absolute_url("ui-exred:landing"),
        get_absolute_url("ui-exred:landing-uk"),
        get_absolute_url("ui-exred:international"),
        get_absolute_url("ui-exred:international-uk"),
        get_absolute_url("ui-exred:international-zh"),
        get_absolute_url("ui-exred:international-de"),
        get_absolute_url("ui-exred:international-ja"),
        get_absolute_url("ui-exred:international-es"),
        get_absolute_url("ui-exred:international-pt"),
        get_absolute_url("ui-exred:international-ar"),
        get_absolute_url("ui-exred:triage-sector"),
        get_absolute_url("ui-exred:triage-exported-before"),
        get_absolute_url("ui-exred:triage-regular-exporter"),
        get_absolute_url("ui-exred:triage-online-marketplace"),
        get_absolute_url("ui-exred:triage-companies-house"),
        get_absolute_url("ui-exred:triage-company"),
        get_absolute_url("ui-exred:triage-summary"),
        get_absolute_url("ui-exred:custom"),
        get_absolute_url("ui-exred:get-finance"),
        get_absolute_url("ui-exred:story-first"),
        get_absolute_url("ui-exred:story-second"),
        get_absolute_url("ui-exred:story-third"),
        get_absolute_url("ui-exred:terms"),
        get_absolute_url("ui-exred:privacy"),
    ],
)
def test_exred_pages(url, basic_auth):
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)


@pytest.mark.parametrize(
    "url,redirect",
    [
        (get_absolute_url("ui-exred:new"), "/advice/"),
        (get_absolute_url("ui-exred:occasional"), "/advice/"),
        (get_absolute_url("ui-exred:regular"), "/advice/"),
        (
            get_absolute_url("ui-exred:market-research"),
            "/advice/find-an-export-market/",
        ),
        (
            get_absolute_url("ui-exred:customer-insight"),
            "/advice/prepare-to-do-business-in-a-foreign-country/",
        ),
        (
            get_absolute_url("ui-exred:finance"),
            "/advice/get-export-finance-and-funding/",
        ),
        (
            get_absolute_url("ui-exred:business-planning"),
            "/advice/define-route-to-market/",
        ),
        (
            get_absolute_url("ui-exred:getting-paid"),
            "/advice/manage-payment-for-export-orders/",
        ),
        (
            get_absolute_url("ui-exred:operations-and-compliance"),
            "/advice/manage-legal-and-ethical-compliance/",
        ),
    ],
)
def test_exred_redirects(url, redirect, basic_auth):
    resp = get_and_assert(url=url, status_code=HTTP_302_FOUND, auth=basic_auth)
    location = resp.headers["location"]
    error = f"Expected redirect to '{redirect}' but got '{location}'"
    assert resp.headers["location"] == redirect, error
