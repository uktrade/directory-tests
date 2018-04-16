import http.client

import pytest
import requests
from tests import get_absolute_url


@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('ui-contact-us:help'),
    get_absolute_url('ui-contact-us:feedback-form'),
    get_absolute_url('ui-contact-us:directory'),
    get_absolute_url('ui-contact-us:directory-feedback-form'),
    get_absolute_url('ui-contact-us:soo-triage'),
    get_absolute_url('ui-contact-us:soo-triage-form'),
    get_absolute_url('ui-contact-us:soo-triage-feedback-form'),
])
def test_access_contact_us_endpoints(absolute_url):
    response = requests.get(absolute_url, allow_redirects=True)
    assert response.status_code == http.client.OK


@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('ui-contact-us:help'),
    get_absolute_url('ui-contact-us:feedback-form'),
    get_absolute_url('ui-contact-us:directory'),
    get_absolute_url('ui-contact-us:directory-feedback-form'),
    get_absolute_url('ui-contact-us:soo-triage'),
    get_absolute_url('ui-contact-us:soo-triage-form'),
    get_absolute_url('ui-contact-us:soo-triage-feedback-form'),
])
def test_access_contact_us_endpoints_without_trailing_slash(
        absolute_url):
    # get rid of trailing slash
    absolute_url = absolute_url[:-1]
    response = requests.get(absolute_url, allow_redirects=True)
    assert response.status_code == http.client.OK


@pytest.mark.parametrize("market", [
    "ebay",
    "etsy",
    "amazon-france",
    "rakuten"
])
def test_get_market_details(market):
    url = get_absolute_url("ui-contact-us:soo-triage-form")
    params = {
        "market": market
    }
    response = requests.get(url, params=params, allow_redirects=True)
    assert response.status_code == http.client.OK


@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('ui-contact-us:feedback-form'),
    get_absolute_url('ui-contact-us:directory-feedback-form'),
])
def test_submit_feedback_form_without_valid_captcha(absolute_url):
    data = {
        "csrfmiddlewaretoken": "invalid_token",
        "originating_page": "Direct request",
        "service": "directory",
        "contact_name": "smoke tests",
        "contact_email": "smoketests@example.com",
        "content": "smoke tests",
        "g-recaptcha-response": "invalid captcha response"
    }
    response = requests.post(absolute_url, data=data, allow_redirects=True)
    assert response.status_code == 403
