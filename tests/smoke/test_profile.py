import http.client

import requests

from tests import get_absolute_url, users


def test_landing_302():
    response = requests.get(
        get_absolute_url('profile:landing'), allow_redirects=False
    )

    assert response.status_code == http.client.FOUND


def test_about_200():
    response = requests.get(
        get_absolute_url('profile:about'), allow_redirects=False
    )

    assert response.status_code == http.client.OK


def test_soo_logged_in_user_200(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('profile:soo'), allow_redirects=False
    )

    assert response.status_code == http.client.OK


def test_soo_anon_user_302():
    response = requests.get(
        get_absolute_url('profile:soo'), allow_redirects=False
    )

    assert response.status_code == http.client.FOUND


def test_fab_logged_in_user_200(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('profile:fab'), allow_redirects=False
    )

    assert response.status_code == http.client.OK


def test_fab_anon_user_302():
    response = requests.get(
        get_absolute_url('profile:fab'), allow_redirects=False
    )

    assert response.status_code == http.client.FOUND


def test_exops_applications_logged_in_user_200(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('profile:exops-applications'), allow_redirects=False
    )

    assert response.status_code == http.client.OK


def test_exops_applications_anon_user_302():
    response = requests.get(
        get_absolute_url('profile:exops-applications'), allow_redirects=False
    )

    assert response.status_code == http.client.FOUND


def test_exops_alerts_logged_in_user_200(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('profile:exops-alerts'), allow_redirects=False
    )

    assert response.status_code == http.client.OK


def test_exops_alerts_anon_user_302():
    response = requests.get(
        get_absolute_url('profile:exops-alerts'), allow_redirects=False
    )

    assert response.status_code == http.client.FOUND


def test_directory_supplier_verified_user():
    token = 'Bearer {token}'.format(token=users['verified']['token'])
    headers = {'Authorization': token}
    url = get_absolute_url('profile:directory-supplier')
    response = requests.get(url, headers=headers)

    assert response.status_code == http.client.OK
    assert response.json() == {
        'company_industries': [],
        'name': 'Testo Useri',
        'company_name': 'Test company 57',
        'company_number': '12345679',
        'sso_id': users['verified']['sso_id'],
        'company_email': 'testo@useri.com',
        'profile_url': 'http://dev.supplier.directory.uktrade.io/'
                       'suppliers/12345679',
        'company_export_status': 'ONE_TWO_YEARS_AGO'
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
