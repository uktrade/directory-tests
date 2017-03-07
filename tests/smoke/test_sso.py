import http.client

import requests

from tests import get_absolute_url


def test_login_200_anon_user():
    response = requests.get(
        get_absolute_url('sso:login'), allow_redirects=False
    )

    assert response.status_code == http.client.OK


def test_login_redirects_logged_in_user(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('sso:login'), allow_redirects=False
    )

    assert response.status_code == http.client.FOUND


def test_signup_200_anon_users():
    response = requests.get(
        get_absolute_url('sso:signup'), allow_redirects=False
    )

    assert response.status_code == http.client.OK


def test_signup_redirects_logged_in_users(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('sso:signup'), allow_redirects=False
    )

    assert response.status_code == http.client.FOUND


def test_logout_200_logged_in_user(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('sso:logout'), allow_redirects=False
    )
    assert response.status_code == http.client.OK


def test_logout_redirects_anon_users():
    response = requests.get(
        get_absolute_url('sso:logout'), allow_redirects=False
    )
    assert response.status_code == http.client.FOUND


def test_password_change_200_logged_in_user(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('sso:password_change'), allow_redirects=False
    )

    assert response.status_code == http.client.OK


def test_password_change_redirects_anon_user():
    response = requests.get(
        get_absolute_url('sso:password_change'), allow_redirects=False
    )

    assert response.status_code == http.client.FOUND


def test_password_reset_200():
    response = requests.get(
        get_absolute_url('sso:password_reset'), allow_redirects=False
    )

    assert response.status_code == http.client.OK
