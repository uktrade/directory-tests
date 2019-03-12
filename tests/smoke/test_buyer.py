import http.client

import pytest
import requests
from retrying import retry

from tests import get_absolute_url, companies, retriable_error


@pytest.mark.skip(reason="ATM we're not caching inactive companies: see "
                         "tickets: ED-3188, ED-3782")
def test_landing_page_post_company_not_active(basic_auth):
    data = {"company_number": companies["not_active"]}
    response = requests.post(
        get_absolute_url("ui-buyer:landing"), data=data, allow_redirects=False,
        auth=basic_auth
    )
    assert "Company not active" in str(response.content)


def test_landing_page_post_company_already_registered(basic_auth):
    data = {"company_number": companies["already_registered"]}
    response = requests.post(
        get_absolute_url("ui-buyer:landing"), data=data, allow_redirects=False,
        auth=basic_auth
    )
    assert "Already registered" in str(response.content)


def test_landing_page_post_company_not_found(basic_auth):
    data = {"company_number": "12345670"}
    response = requests.post(
        get_absolute_url("ui-buyer:landing"), data=data, allow_redirects=False,
        auth=basic_auth
    )
    assert "Error. Please try again later." in str(response.content)


def test_landing_page_post_company_happy_path(basic_auth):
    data = {"company_number": companies["active_not_registered"]}
    response = requests.post(
        get_absolute_url("ui-buyer:landing"),
        data=data,
        auth=basic_auth
    )
    assert "Register" in str(response.content)


def test_not_existing_page_return_404_anon_user(basic_auth):
    url = get_absolute_url("ui-buyer:landing") + "/foobar"
    response = requests.get(url, allow_redirects=False, auth=basic_auth)
    assert response.status_code == 404


@pytest.mark.session_auth
def test_not_existing_page_return_404_user(logged_in_session, basic_auth):
    url = get_absolute_url("ui-buyer:landing") + "/foobar"
    response = logged_in_session.get(
        url, allow_redirects=False, auth=basic_auth
    )
    assert response.status_code == 404


@retry(
    wait_fixed=30000,
    stop_max_attempt_number=2,
    retry_on_exception=retriable_error,
)
@pytest.mark.parametrize("absolute_url", [
    get_absolute_url("ui-buyer:register"),
    get_absolute_url("ui-buyer:register-confirm-export-status"),
    get_absolute_url("ui-buyer:register-submit-account-details"),
    get_absolute_url("ui-buyer:case-study-create"),
    get_absolute_url("ui-buyer:case-study-edit"),
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
])
def test_301_redirects_for_anon_user(absolute_url, basic_auth):
    response = requests.get(
        absolute_url, allow_redirects=False, auth=basic_auth
    )
    assert response.status_code == http.client.FOUND


@retry(
    wait_fixed=30000,
    stop_max_attempt_number=2,
    retry_on_exception=retriable_error,
)
@pytest.mark.parametrize("absolute_url", [
    get_absolute_url("ui-buyer:register-confirm-company"),
    get_absolute_url("ui-buyer:register-confirm-export-status"),
    get_absolute_url("ui-buyer:register-finish"),
    get_absolute_url("ui-buyer:register-submit-account-details"),
    get_absolute_url("ui-buyer:case-study-create"),
    get_absolute_url("ui-buyer:case-study-edit"),
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
])
def test_302_redirects_after_removing_trailing_slash_for_anon_user(
        absolute_url, basic_auth):
    # get rid of trailing slash
    absolute_url = absolute_url[:-1]
    response = requests.get(
        absolute_url, allow_redirects=False, auth=basic_auth
    )
    assert response.status_code == http.client.MOVED_PERMANENTLY


@pytest.mark.session_auth
@retry(
    wait_fixed=30000,
    stop_max_attempt_number=2,
    retry_on_exception=retriable_error,
)
@pytest.mark.parametrize("absolute_url", [
    get_absolute_url("ui-buyer:landing"),
    get_absolute_url("ui-buyer:register"),
    get_absolute_url("ui-buyer:register-confirm-company"),
    get_absolute_url("ui-buyer:register-confirm-export-status"),
    get_absolute_url("ui-buyer:register-finish"),
    get_absolute_url("ui-buyer:register-submit-account-details"),
    get_absolute_url("ui-buyer:upload-logo"),
    get_absolute_url("ui-buyer:case-study-create"),
    get_absolute_url("ui-buyer:case-study-edit"),
    get_absolute_url("ui-buyer:confirm-company-address"),
    get_absolute_url("ui-buyer:confirm-identity"),
    get_absolute_url("ui-buyer:confirm-identity-letter"),
    get_absolute_url("ui-buyer:company-profile"),
    get_absolute_url("ui-buyer:company-edit"),
    get_absolute_url("ui-buyer:company-edit-address"),
    get_absolute_url("ui-buyer:company-edit-description"),
    get_absolute_url("ui-buyer:company-edit-key-facts"),
    get_absolute_url("ui-buyer:company-edit-sectors"),
    get_absolute_url("ui-buyer:company-edit-contact"),
    get_absolute_url("ui-buyer:company-edit-social-media"),
])
def test_access_non_health_check_endpoints_as_logged_in_user(
        logged_in_session, absolute_url, basic_auth):
    response = logged_in_session.get(
        absolute_url, allow_redirects=True, auth=basic_auth
    )
    assert response.status_code == http.client.OK
