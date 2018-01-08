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

    assert response.status_code == http.client.OK
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

    assert response.status_code == http.client.NOT_FOUND


def test_directory_supplier_invalid_user_token():
    token = 'Bearer {token}'.format(token='foo')
    headers = {'Authorization': token}
    url = get_absolute_url('profile:directory-supplier')
    response = requests.get(url, headers=headers)

    assert response.status_code == 401


@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('profile:healthcheck-api'),
    get_absolute_url('profile:healthcheck-sso-proxy'),
])
def test_health_check_endpoints(absolute_url):
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
    assert response.status_code == http.client.FOUND


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
    assert response.status_code == http.client.MOVED_PERMANENTLY


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
    assert response.status_code == http.client.OK
