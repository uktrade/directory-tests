import http.client

import requests

from tests import get_absolute_url, companies


def test_landing_page_200():
    response = requests.get(
        get_absolute_url('ui-buyer:landing'), allow_redirects=False
    )

    assert response.status_code == http.client.OK


def test_landing_page_post_company_not_active():
    data = {'company_number': companies['not_active']}
    response = requests.post(
        get_absolute_url('ui-buyer:landing'), data=data, allow_redirects=False
    )
    assert 'Company not active' in str(response.content)


def test_landing_page_post_company_already_registered():
    data = {'company_number': companies['already_registered']}
    response = requests.post(
        get_absolute_url('ui-buyer:landing'), data=data, allow_redirects=False
    )
    assert 'Already registered' in str(response.content)


def test_landing_page_post_company_not_found():
    data = {'company_number': '12345670'}
    response = requests.post(
        get_absolute_url('ui-buyer:landing'), data=data, allow_redirects=False
    )
    assert 'Error. Please try again later.' in str(response.content)


def test_landing_page_post_company_happy_path():
    data = {'company_number': companies['active_not_registered']}
    response = requests.post(
        get_absolute_url('ui-buyer:landing'),
        data=data
    )

    assert 'Register' in str(response.content)


def test_enrolment_instructions_302_anon_user():
    response = requests.get(
        get_absolute_url('ui-buyer:register'), allow_redirects=False
    )

    assert response.status_code == http.client.FOUND


def test_enrolment_redirects_company_user(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('ui-buyer:register'), allow_redirects=False
    )

    assert response.status_code == http.client.FOUND


def test_profile_redirects_anon_user():
    response = requests.get(
        get_absolute_url('ui-buyer:company-profile'), allow_redirects=False
    )

    assert response.status_code == http.client.FOUND


def test_enrolment_200_company_user(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('ui-buyer:company-profile'), allow_redirects=False
    )

    assert response.status_code == http.client.OK


def test_profile_logo_edit_redirects_anon_user():
    response = requests.get(
        get_absolute_url('ui-buyer:upload-logo'), allow_redirects=False
    )

    assert response.status_code == http.client.FOUND


def test_profile_logo_edit_200_company_user(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('ui-buyer:upload-logo'), allow_redirects=False
    )

    assert response.status_code == http.client.OK


def test_profile_address_edit_redirects_anon_user():
    response = requests.get(
        get_absolute_url('ui-buyer:company-edit-address'),
        allow_redirects=False
    )

    assert response.status_code == http.client.FOUND


def test_profile_address_edit_200_company_user(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('ui-buyer:company-edit-address'),
        allow_redirects=False
    )

    assert response.status_code == http.client.OK


def test_profile_description_edit_redirects_anon_user():
    response = requests.get(
        get_absolute_url('ui-buyer:company-edit-description'),
        allow_redirects=False
    )

    assert response.status_code == http.client.FOUND


def test_profile_description_edit_200_company_user(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('ui-buyer:company-edit-description'),
        allow_redirects=False
    )

    assert response.status_code == http.client.OK


def test_profile_key_facts_edit_redirects_anon_user():
    response = requests.get(
        get_absolute_url('ui-buyer:company-edit-key-facts'),
        allow_redirects=False
    )

    assert response.status_code == http.client.FOUND


def test_profile_key_facts_edit_200_company_user(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('ui-buyer:company-edit-key-facts'),
        allow_redirects=False
    )

    assert response.status_code == http.client.OK


def test_profile_sectors_edit_redirects_anon_user():
    response = requests.get(
        get_absolute_url('ui-buyer:company-edit-sectors'),
        allow_redirects=False
    )

    assert response.status_code == http.client.FOUND


def test_profile_sectors_edit_200_company_user(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('ui-buyer:company-edit-sectors'),
        allow_redirects=False
    )

    assert response.status_code == http.client.OK


def test_profile_contact_edit_redirects_anon_user():
    response = requests.get(
        get_absolute_url('ui-buyer:company-edit-contact'),
        allow_redirects=False
    )

    assert response.status_code == http.client.FOUND


def test_profile_contact_edit_200_company_user(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('ui-buyer:company-edit-contact'),
        allow_redirects=False
    )

    assert response.status_code == http.client.OK


def test_profile_social_media_edit_redirects_anon_user():
    response = requests.get(
        get_absolute_url('ui-buyer:company-edit-social-media'),
        allow_redirects=False
    )

    assert response.status_code == http.client.FOUND


def test_profile_social_media_edit_200_company_user(logged_in_session):
    response = logged_in_session.get(
        get_absolute_url('ui-buyer:company-edit-social-media'),
        allow_redirects=False
    )

    assert response.status_code == http.client.OK


def test_not_existing_page_return_404_anon_user():
    url = get_absolute_url('ui-buyer:landing') + '/foobar'
    response = requests.get(url, allow_redirects=False)

    assert response.status_code == 404


def test_not_existing_page_return_404_user(logged_in_session):
    url = get_absolute_url('ui-buyer:landing') + '/foobar'
    response = logged_in_session.get(url, allow_redirects=False)

    assert response.status_code == 404
