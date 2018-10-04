import http.client

import pytest
import requests

from tests import get_absolute_url, users
from tests.settings import DIRECTORY_API_HEALTH_CHECK_TOKEN as TOKEN


def test_about_200():
    response = requests.get(
        get_absolute_url('profile:about'), allow_redirects=False
    )

    assert response.status_code == http.client.OK


def test_directory_supplier_verified_user():
    token = 'Bearer {token}'.format(token=users['verified']['token'])
    headers = {'Authorization': token}
    url = get_absolute_url('profile:directory-supplier')
    response = requests.get(url, headers=headers)

    error_msg = f"Expected 200 got {response.status_code} from {response.url}"
    assert response.status_code == http.client.OK, error_msg
    assert response.json() == {
        'company_industries': [
            "BUSINESS_AND_CONSUMER_SERVICES", "COMMUNICATIONS",
            "CREATIVE_AND_MEDIA", "FINANCIAL_AND_PROFESSIONAL_SERVICES",
            "HEALTHCARE_AND_MEDICAL", "RAILWAYS",
            "SOFTWARE_AND_COMPUTER_SERVICES"
        ],
        'name': 'Test user 50',
        'company_name': 'Tiramisu Design Consultants',
        'company_number': '07619397',
        'sso_id': users['verified']['sso_id'],
        'company_email': 'newverifieduser@example.com',
        'profile_url': 'https://dev.supplier.directory.uktrade.io/'
                       'suppliers/07619397',
        'company_has_exported_before': True,
        'is_company_owner': True,
    }


def test_directory_supplier_unverified_user():
    token = 'Bearer {token}'.format(token=users['unverified']['token'])
    headers = {'Authorization': token}
    url = get_absolute_url('profile:directory-supplier')
    response = requests.get(url, headers=headers)

    error_msg = f"Expected 404 got {response.status_code} from {response.url}"
    assert response.status_code == http.client.NOT_FOUND, error_msg


def test_directory_supplier_invalid_user_token():
    token = 'Bearer {token}'.format(token='foo')
    headers = {'Authorization': token}
    url = get_absolute_url('profile:directory-supplier')
    response = requests.get(url, headers=headers)

    error_msg = f"Expected 401 got {response.status_code} from {response.url}"
    assert response.status_code == 401, error_msg


@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('profile:healthcheck-ping'),
])
def test_health_check_endpoints(absolute_url):
    response = requests.get(absolute_url)
    assert response.status_code == http.client.OK


@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('profile:healthcheck-ping'),
    get_absolute_url('profile:healthcheck-sentry'),
    get_absolute_url('profile:healthcheck-sso'),
])
def test_health_check_endpoints_auth(absolute_url):
    params = {'token': TOKEN}
    response = requests.get(absolute_url, params=params)
    assert response.status_code == http.client.OK


@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('profile:landing'),
    get_absolute_url('profile:soo'),
    get_absolute_url('profile:fab'),
    get_absolute_url('profile:exops-alerts'),
    get_absolute_url('profile:exops-applications'),
])
def test_301_redirects_for_anon_user(absolute_url):
    response = requests.get(absolute_url, allow_redirects=False)
    error_msg = f"Expected 301 got {response.status_code} from {response.url}"
    assert response.status_code == http.client.FOUND, error_msg


@pytest.mark.skip(reason="see bug ED-3050")
@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('profile:soo'),
    get_absolute_url('profile:fab'),
    get_absolute_url('profile:exops-alerts'),
    get_absolute_url('profile:exops-applications'),
])
def test_302_redirects_after_removing_trailing_slash_for_anon_user(absolute_url):
    # get rid of trailing slash
    if absolute_url[-1] == "/":
        absolute_url = absolute_url[:-1]
    response = requests.get(absolute_url, allow_redirects=False)
    error_msg = f"Expected 302 got {response.status_code} from {response.url}"
    assert response.status_code == http.client.MOVED_PERMANENTLY, error_msg


@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('profile:directory-supplier'),
])
def test_401_redirects_for_anon_user(absolute_url):
    response = requests.get(absolute_url, allow_redirects=False)
    assert response.status_code == 401


@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('profile:landing'),
    get_absolute_url('profile:soo'),
    get_absolute_url('profile:fab'),
    get_absolute_url('profile:exops-alerts'),
    get_absolute_url('profile:exops-applications'),
])
def test_access_to_non_health_check_endpoints_as_logged_in_user(
        logged_in_session, absolute_url):
    response = logged_in_session.get(absolute_url, allow_redirects=True)
    error_msg = f"Expected 200 got {response.status_code} from {response.url}"
    assert response.status_code == http.client.OK, error_msg
