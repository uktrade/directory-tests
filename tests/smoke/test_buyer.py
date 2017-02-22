import httplib

import requests

from tests import get_absolute_url


def test_landing_page_200():
    response = requests.get(
        get_absolute_url('ui-buyer:landing'), allow_redirects=False
    )

    assert response.status_code == httplib.OK


def test_enrolment_200_anon_user():
    response = requests.get(
        get_absolute_url('ui-buyer:register'), allow_redirects=False
    )

    assert response.status_code == httplib.OK



def test_enrolment_redirects_company_user(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('ui-buyer:register'), allow_redirects=False
    )

    assert response.status_code == httplib.FOUND


def test_profile_redirects_anon_user():
    response = requests.get(
        get_absolute_url('ui-buyer:company-profile'), allow_redirects=False
    )

    assert response.status_code == httplib.FOUND


def test_enrolment_200_company_user(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('ui-buyer:company-profile'), allow_redirects=False
    )

    assert response.status_code == httplib.OK


def test_profile_logo_edit_redirects_anon_user():
    response = requests.get(
        get_absolute_url('ui-buyer:upload-logo'), allow_redirects=False
    )

    assert response.status_code == httplib.FOUND



def test_profile_logo_edit_200_company_user(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('ui-buyer:upload-logo'), allow_redirects=False
    )

    assert response.status_code == httplib.OK


def test_profile_address_edit_redirects_anon_user():
    response = requests.get(
        get_absolute_url('ui-buyer:company-edit-address'), allow_redirects=False
    )

    assert response.status_code == httplib.FOUND


def test_profile_address_edit_200_company_user(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('ui-buyer:company-edit-address'), allow_redirects=False
    )

    assert response.status_code == httplib.OK

def test_profile_description_edit_redirects_anon_user():
    response = requests.get(
        get_absolute_url('ui-buyer:company-edit-description'), allow_redirects=False
    )

    assert response.status_code == httplib.FOUND


def test_profile_description_edit_200_company_user(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('ui-buyer:company-edit-description'), allow_redirects=False
    )

    assert response.status_code == httplib.OK


def test_profile_key_facts_edit_redirects_anon_user():
    response = requests.get(
        get_absolute_url('ui-buyer:company-edit-key-facts'), allow_redirects=False
    )

    assert response.status_code == httplib.FOUND


def test_profile_key_facts_edit_200_company_user(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('ui-buyer:company-edit-key-facts'), allow_redirects=False
    )

    assert response.status_code == httplib.OK


def test_profile_sectors_edit_redirects_anon_user():
    response = requests.get(
        get_absolute_url('ui-buyer:company-edit-sectors'), allow_redirects=False
    )

    assert response.status_code == httplib.FOUND


def test_profile_sectors_edit_200_company_user(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('ui-buyer:company-edit-sectors'), allow_redirects=False
    )

    assert response.status_code == httplib.OK


def test_profile_contact_edit_redirects_anon_user():
    response = requests.get(
        get_absolute_url('ui-buyer:company-edit-contact'), allow_redirects=False
    )

    assert response.status_code == httplib.FOUND


def test_profile_contact_edit_200_company_user(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('ui-buyer:company-edit-contact'), allow_redirects=False
    )

    assert response.status_code == httplib.OK


def test_profile_social_media_edit_redirects_anon_user():
    response = requests.get(
        get_absolute_url('ui-buyer:company-edit-social-media'), allow_redirects=False
    )

    assert response.status_code == httplib.FOUND


def test_profile_social_media_edit_200_company_user(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('ui-buyer:company-edit-social-media'), allow_redirects=False
    )

    assert response.status_code == httplib.OK
