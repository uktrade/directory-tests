import http.client

import pytest
import requests
from mohawk import Sender
from retrying import retry

from tests import get_absolute_url, companies, retriable_error
from tests.settings import DIRECTORY_API_HEALTH_CHECK_TOKEN as TOKEN
from tests.settings import (
    IP_RESTRICTOR_SKIP_CHECK_SENDER_ID,
    IP_RESTRICTOR_SKIP_CHECK_SECRET,
)


def get_hawk_authorization_signature(method: str = 'GET'):
    sender = Sender(
        credentials={
            'id': IP_RESTRICTOR_SKIP_CHECK_SENDER_ID,
            'key': IP_RESTRICTOR_SKIP_CHECK_SECRET,
            'algorithm': 'sha256'
        },
        url='/',
        method=method,
        always_hash_content=False
    )
    return {"Authorization": sender.request_header}


@pytest.mark.skip(reason="ATM we're not caching inactive companies: see "
                         "tickets: ED-3188, ED-3782")
def test_landing_page_post_company_not_active():
    data = {'company_number': companies['not_active']}
    response = requests.post(
        get_absolute_url('ui-buyer:landing'), data=data, allow_redirects=False
    )
    assert 'Company not active' in str(response.content)


def test_landing_page_post_company_already_registered():
    data = {'company_number': companies['already_registered']}
    auth_header = get_hawk_authorization_signature(method='POST')
    response = requests.post(
        get_absolute_url('ui-buyer:landing'), data=data, allow_redirects=False,
        headers=auth_header
    )
    print(response.request.headers)
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


def test_not_existing_page_return_404_anon_user():
    url = get_absolute_url('ui-buyer:landing') + '/foobar'
    response = requests.get(url, allow_redirects=False)
    assert response.status_code == 404


def test_not_existing_page_return_404_user(logged_in_session):
    url = get_absolute_url('ui-buyer:landing') + '/foobar'
    response = logged_in_session.get(url, allow_redirects=False)
    assert response.status_code == 404


@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('ui-buyer:healthcheck-api'),
    get_absolute_url('ui-buyer:healthcheck-sso'),
])
def test_health_check_endpoints(absolute_url):
    params = {'token': TOKEN}
    response = requests.get(absolute_url, params=params)
    assert response.status_code == http.client.OK


@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('ui-buyer:healthcheck-api'),
    get_absolute_url('ui-buyer:healthcheck-sso'),
])
def test_redirects_for_health_check_endpoints(absolute_url):
    params = {'token': TOKEN}
    # get rid of trailing slash
    absolute_url = absolute_url[:-1]
    response = requests.get(absolute_url, params=params, allow_redirects=False)
    assert response.status_code == http.client.MOVED_PERMANENTLY


@retry(
    wait_fixed=30000,
    stop_max_attempt_number=2,
    retry_on_exception=retriable_error,
)
@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('ui-buyer:register'),
    get_absolute_url('ui-buyer:register-confirm-export-status'),
    get_absolute_url('ui-buyer:register-submit-account-details'),
    get_absolute_url('ui-buyer:case-study-create'),
    get_absolute_url('ui-buyer:case-study-edit'),
    get_absolute_url('ui-buyer:confirm-company-address'),
    get_absolute_url('ui-buyer:confirm-identity'),
    get_absolute_url('ui-buyer:confirm-identity-letter'),
    get_absolute_url('ui-buyer:company-profile'),
    get_absolute_url('ui-buyer:company-edit'),
    get_absolute_url('ui-buyer:company-edit-description'),
    get_absolute_url('ui-buyer:company-edit-key-facts'),
    get_absolute_url('ui-buyer:company-edit-sectors'),
    get_absolute_url('ui-buyer:company-edit-contact'),
    get_absolute_url('ui-buyer:company-edit-social-media'),
])
def test_301_redirects_for_anon_user(absolute_url):
    response = requests.get(absolute_url, allow_redirects=False)
    assert response.status_code == http.client.FOUND


@retry(
    wait_fixed=30000,
    stop_max_attempt_number=2,
    retry_on_exception=retriable_error,
)
@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('ui-buyer:healthcheck-api'),
    get_absolute_url('ui-buyer:healthcheck-sso'),
    get_absolute_url('ui-buyer:register-confirm-company'),
    get_absolute_url('ui-buyer:register-confirm-export-status'),
    get_absolute_url('ui-buyer:register-finish'),
    get_absolute_url('ui-buyer:register-submit-account-details'),
    get_absolute_url('ui-buyer:case-study-create'),
    get_absolute_url('ui-buyer:case-study-edit'),
    get_absolute_url('ui-buyer:confirm-company-address'),
    get_absolute_url('ui-buyer:confirm-identity'),
    get_absolute_url('ui-buyer:confirm-identity-letter'),
    get_absolute_url('ui-buyer:company-profile'),
    get_absolute_url('ui-buyer:company-edit'),
    get_absolute_url('ui-buyer:company-edit-description'),
    get_absolute_url('ui-buyer:company-edit-key-facts'),
    get_absolute_url('ui-buyer:company-edit-sectors'),
    get_absolute_url('ui-buyer:company-edit-contact'),
    get_absolute_url('ui-buyer:company-edit-social-media'),
])
def test_302_redirects_after_removing_trailing_slash_for_anon_user(
        absolute_url):
    # get rid of trailing slash
    absolute_url = absolute_url[:-1]
    response = requests.get(absolute_url, allow_redirects=False)
    assert response.status_code == http.client.MOVED_PERMANENTLY


@retry(
    wait_fixed=30000,
    stop_max_attempt_number=2,
    retry_on_exception=retriable_error,
)
@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('ui-buyer:landing'),
    get_absolute_url('ui-buyer:register'),
    get_absolute_url('ui-buyer:register-confirm-company'),
    get_absolute_url('ui-buyer:register-confirm-export-status'),
    get_absolute_url('ui-buyer:register-finish'),
    get_absolute_url('ui-buyer:register-submit-account-details'),
    get_absolute_url('ui-buyer:upload-logo'),
    get_absolute_url('ui-buyer:case-study-create'),
    get_absolute_url('ui-buyer:case-study-edit'),
    get_absolute_url('ui-buyer:confirm-company-address'),
    get_absolute_url('ui-buyer:confirm-identity'),
    get_absolute_url('ui-buyer:confirm-identity-letter'),
    get_absolute_url('ui-buyer:company-profile'),
    get_absolute_url('ui-buyer:company-edit'),
    get_absolute_url('ui-buyer:company-edit-address'),
    get_absolute_url('ui-buyer:company-edit-description'),
    get_absolute_url('ui-buyer:company-edit-key-facts'),
    get_absolute_url('ui-buyer:company-edit-sectors'),
    get_absolute_url('ui-buyer:company-edit-contact'),
    get_absolute_url('ui-buyer:company-edit-social-media'),
])
def test_access_non_health_check_endpoints_as_logged_in_user(
        logged_in_session, absolute_url):
    response = logged_in_session.get(absolute_url, allow_redirects=True)
    assert response.status_code == http.client.OK
