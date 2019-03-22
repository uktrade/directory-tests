import pytest
import requests
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_301_MOVED_PERMANENTLY,
    HTTP_302_FOUND,
    HTTP_404_NOT_FOUND,
)

from tests import companies, get_absolute_url
from tests.smoke.cms_api_helpers import get_and_assert, status_error


@pytest.mark.skip(
    reason="ATM we're not caching inactive companies: see "
    "tickets: ED-3188, ED-3782"
)
def test_landing_page_post_company_not_active(basic_auth):
    data = {"company_number": companies["not_active"]}
    response = requests.post(
        get_absolute_url("ui-buyer:landing"),
        data=data,
        allow_redirects=False,
        auth=basic_auth,
    )
    assert "Company not active" in str(response.content)


@pytest.mark.session_auth
def test_not_existing_page_return_404_user(logged_in_session, basic_auth):
    url = get_absolute_url("ui-buyer:landing") + "/foobar"
    response = logged_in_session.get(
        url, allow_redirects=False, auth=basic_auth
    )
    assert response.status_code == HTTP_404_NOT_FOUND, status_error(
        HTTP_404_NOT_FOUND, response
    )


@pytest.mark.parametrize(
    "url,destination",
    [
        (
            get_absolute_url("ui-buyer:register"),
            get_absolute_url("ui-buyer:landing"),
        )
    ],
)
def test_redirects_to_profile_pages(url, destination, basic_auth):
    response = get_and_assert(
        url=url,
        allow_redirects=False,
        status_code=HTTP_302_FOUND,
        auth=basic_auth,
    )
    location = response.headers["location"]
    assert destination.endswith(location)


@pytest.mark.parametrize(
    "url",
    [
        get_absolute_url("ui-buyer:register"),
        get_absolute_url("ui-buyer:register-confirm-export-status"),
        get_absolute_url("ui-buyer:register-submit-account-details"),
        get_absolute_url("ui-buyer:confirm-company-address"),
        get_absolute_url("ui-buyer:confirm-identity"),
        get_absolute_url("ui-buyer:confirm-identity-letter"),
        get_absolute_url("ui-buyer:company-profile"),
        get_absolute_url("ui-buyer:company-edit"),
        get_absolute_url("ui-buyer:company-edit-description"),
        get_absolute_url("ui-buyer:company-edit-key-facts"),
        get_absolute_url("ui-buyer:company-edit-sectors"),
        get_absolute_url("ui-buyer:company-edit-contact"),
        get_absolute_url("ui-buyer:company-edit-social-media"),
    ],
)
def test_302_redirects_for_anon_user(url, basic_auth):
    get_and_assert(
        url=url,
        allow_redirects=False,
        status_code=HTTP_302_FOUND,
        auth=basic_auth,
    )


@pytest.mark.parametrize(
    "url",
    [
        get_absolute_url("ui-buyer:register-confirm-company"),
        get_absolute_url("ui-buyer:register-confirm-export-status"),
        get_absolute_url("ui-buyer:register-finish"),
        get_absolute_url("ui-buyer:register-submit-account-details"),
        get_absolute_url("ui-buyer:confirm-company-address"),
        get_absolute_url("ui-buyer:confirm-identity"),
        get_absolute_url("ui-buyer:confirm-identity-letter"),
        get_absolute_url("ui-buyer:company-profile"),
        get_absolute_url("ui-buyer:company-edit"),
        get_absolute_url("ui-buyer:company-edit-description"),
        get_absolute_url("ui-buyer:company-edit-key-facts"),
        get_absolute_url("ui-buyer:company-edit-sectors"),
        get_absolute_url("ui-buyer:company-edit-contact"),
        get_absolute_url("ui-buyer:company-edit-social-media"),
    ],
)
def test_301_redirects_after_removing_trailing_slash_for_anon_user(
    url, basic_auth
):
    # get rid of trailing slash
    if url[-1] == "/":
        url = url[:-1]
    get_and_assert(
        url=url,
        allow_redirects=False,
        status_code=HTTP_301_MOVED_PERMANENTLY,
        auth=basic_auth,
    )


@pytest.mark.session_auth
@pytest.mark.parametrize(
    "url",
    [
        get_absolute_url("ui-buyer:landing"),
        get_absolute_url("ui-buyer:register"),
        get_absolute_url("ui-buyer:register-confirm-company"),
        get_absolute_url("ui-buyer:register-confirm-export-status"),
        get_absolute_url("ui-buyer:register-finish"),
        get_absolute_url("ui-buyer:confirm-company-address"),
        get_absolute_url("ui-buyer:confirm-identity"),
        get_absolute_url("ui-buyer:confirm-identity-letter"),
    ],
)
def test_access_non_health_check_endpoints_as_logged_in_user(
    url, logged_in_session, basic_auth
):
    response = logged_in_session.get(
        url, allow_redirects=True, auth=basic_auth
    )
    assert response.status_code == HTTP_200_OK, status_error(
        HTTP_200_OK, response
    )
