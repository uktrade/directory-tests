import http.client

import requests

from tests import get_absolute_url


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
