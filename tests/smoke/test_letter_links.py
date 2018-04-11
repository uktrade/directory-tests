import http.client

import pytest
import requests

from tests import get_absolute_url


@pytest.mark.parametrize("absolute_url", [
    get_absolute_url("ui-contact-us:help"),
    get_absolute_url("ui-contact-us:feedback-form"),
])
def test_access_as_anon_user(absolute_url):
    response = requests.get(absolute_url, allow_redirects=False)
    assert response.status_code == http.client.OK


@pytest.mark.parametrize("absolute_url", [
    get_absolute_url("ui-contact-us:help"),
    get_absolute_url("ui-contact-us:feedback-form"),
])
def test_access_contact_us_as_anon_user_after_removing_trailing_slash(
        absolute_url):
    # get rid of trailing slash
    absolute_url = absolute_url[:-1]
    response = requests.get(absolute_url, allow_redirects=False)
    assert response.status_code == http.client.OK


@pytest.mark.parametrize("absolute_url", [
    get_absolute_url("ui-buyer:confirm-identity"),
])
def test_302_redirects_for_anon_user(
        absolute_url):
    response = requests.get(absolute_url, allow_redirects=False)
    assert response.status_code == http.client.FOUND


@pytest.mark.parametrize("absolute_url", [
    get_absolute_url("ui-buyer:confirm-identity"),
])
def test_301_redirects_after_removing_trailing_slash_for_anon_user(
        absolute_url):
    # get rid of trailing slash
    absolute_url = absolute_url[:-1]
    response = requests.get(absolute_url, allow_redirects=False)
    assert response.status_code == http.client.MOVED_PERMANENTLY


@pytest.mark.parametrize("absolute_url", [
    get_absolute_url("ui-contact-us:help"),
    get_absolute_url("ui-contact-us:feedback-form"),
    get_absolute_url("ui-buyer:confirm-identity"),
])
def test_access_endpoints_as_logged_in_user(
        logged_in_session, absolute_url):
    response = logged_in_session.get(absolute_url, allow_redirects=True)
    assert response.status_code == http.client.OK


@pytest.mark.parametrize("absolute_url", [
    get_absolute_url("ui-contact-us:help"),
    get_absolute_url("ui-contact-us:feedback-form"),
])
def test_access_endpoints_as_logged_in_user_do_not_follow_redirects(
        logged_in_session, absolute_url):
    response = logged_in_session.get(absolute_url, allow_redirects=False)
    assert response.status_code == http.client.OK


@pytest.mark.parametrize("absolute_url", [
    get_absolute_url("ui-buyer:confirm-identity"),
])
def test_check_if_verify_endpoint_redirects_to_correct_page(
        logged_in_session, absolute_url):
    response = logged_in_session.get(absolute_url, allow_redirects=True)
    assert response.status_code == http.client.OK
    assert response.url == get_absolute_url("ui-buyer:confirm-company-address")
