import httplib

import pytest
import requests

from tests import get_absolute_url, users


@pytest.fixture
def logged_in_session():
    session = requests.Session()
    user = users['verified']
    response = session.post(
        url=get_absolute_url('sso:login'),
        data={'login': user['username'], 'password': user['password']}
    )
    assert 'Logout' in response.content
    return session


def test_login_200_anon_user():
    response = requests.get(
        get_absolute_url('sso:login'), allow_redirects=False
    )

    assert response.status_code == httplib.OK


def test_login_redirects_logged_in_user(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('sso:login'), allow_redirects=False
    )

    assert response.status_code == httplib.FOUND


def test_signup_200_anon_users():
    response = requests.get(
        get_absolute_url('sso:signup'), allow_redirects=False
    )

    assert response.status_code == httplib.OK


def test_signup_redirects_logged_in_users(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('sso:signup'), allow_redirects=False
    )

    assert response.status_code == httplib.FOUND


def test_logout_200_logged_in_user(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('sso:logout'), allow_redirects=False
    )
    assert response.status_code == httplib.OK


def test_logout_redirects_anon_users():
    response = requests.get(
        get_absolute_url('sso:logout'), allow_redirects=False
    )
    assert response.status_code == httplib.FOUND


def test_password_change_200_logged_in_user(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('sso:password_change'), allow_redirects=False
    )

    assert response.status_code == httplib.OK


def test_password_change_redirects_anon_user():
    response = requests.get(
        get_absolute_url('sso:password_change'), allow_redirects=False
    )

    assert response.status_code == httplib.FOUND


def test_password_reset_200():
    response = requests.get(
        get_absolute_url('sso:password_reset'), allow_redirects=False
    )

    assert response.status_code == httplib.OK
