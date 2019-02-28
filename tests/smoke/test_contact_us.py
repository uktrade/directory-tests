import pytest
import requests


from tests.settings import DIRECTORY_LEGACY_CONTACT_US_UI_URL


@pytest.mark.parametrize("endpoint, expected_redirect", [
    ("contact/",                                "/contact/triage/location/"),
    ("directory/",                              "/contact/triage/location/"),
    ("directory/FeedbackForm/",                 "/contact/feedback/"),
    ("eig/",                                    "/contact/triage/location/"),
    ("export-opportunities/FeedbackForm/",      "/contact/feedback/"),
    ("export_opportunities/",                   "/contact/triage/domestic/"),
    ("export_opportunities/FeedbackForm/",      "/contact/feedback/"),
    ("export_ops/",                             "/contact/triage/domestic/"),
    ("export_readiness/FeedbackForm/",          "/contact/feedback/"),
    ("feedback/",                               "/contact/feedback/"),
    ("feedback/datahub/",                       "/contact/feedback/"),
    ("feedback/directory/",                     "/contact/feedback/"),
    ("feedback/e_navigator/",                   "/contact/feedback/"),
    ("feedback/eig/",                           "/contact/feedback/"),
    ("feedback/export_ops/",                    "/contact/feedback/"),
    ("feedback/exportingisgreat/",              "/contact/feedback/"),
    ("feedback/exportopportunities/",           "/contact/feedback/"),
    ("feedback/invest/",                        "/contact/feedback/"),
    ("feedback/opportunities/",                 "/contact/feedback/"),
    ("feedback/selling-online-overseas/",       "/contact/feedback/"),
    ("feedback/selling_online_overseas/",       "/contact/feedback/"),
    ("feedback/single_sign_on/",                "/contact/feedback/"),
    ("feedback/soo/",                           "/contact/feedback/"),
    ("feedback/sso/",                           "/contact/feedback/"),
    ("help/",                                   "/contact/triage/location/"),
    ("help/FeedbackForm/",                      "/contact/feedback/"),
    ("invest/FeedbackForm/",                    "/contact/feedback/"),
    ("opportunities/FeedbackForm/",             "/contact/feedback/"),
    ("selling_online_overseas/",                "/contact/triage/domestic/"),
    ("selling_online_overseas/FeedbackForm/",   "/contact/feedback/"),
    ("single_sign_on/",                         "/contact/triage/great-account/"),
    ("single_sign_on/FeedbackForm/",            "/contact/feedback/"),
    ("soo/FeedbackForm/",                       "/contact/feedback/"),
    ("soo/Triage/",                             "/contact/triage/location/"),
    ("soo/TriageForm/",                         "/contact/selling-online-overseas/organisation/"),
    ("soo/feedback/",                           "/contact/feedback/"),
    ("triage/",                                 "/contact/triage/location/"),
    ("triage/directory/",                       "/contact/triage/location/"),
    ("triage/soo/",                             "/contact/selling-online-overseas/organisation/"),
    ("triage/sso/",                             "/contact/triage/location/"),
])
def test_redirects_for_legacy_contact_us_urls(
        endpoint, expected_redirect, hawk_cookie
):
    url = DIRECTORY_LEGACY_CONTACT_US_UI_URL + endpoint
    response = requests.get(url, allow_redirects=True, cookies=hawk_cookie)
    error_message = f"Expected 200 OK but got {response.status_code} from {url}"
    assert response.status_code == 200, error_message
    if response.history:
        redirects = [h.headers['Location'] for h in response.history]
        last_redirect = redirects[-1]
        error_message = (f"Expected {url} redirect to: '{expected_redirect}' "
                         f"but got {last_redirect}")
        assert expected_redirect == last_redirect, error_message


