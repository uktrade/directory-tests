import pytest
import requests
from http.client import OK, MOVED_PERMANENTLY

from directory_cms_client.client import cms_api_client
from directory_sso_api_client.client import sso_api_client
from retrying import retry

from tests import get_absolute_url, retriable_error, get_relative_url
from tests.settings import DIRECTORY_API_HEALTH_CHECK_TOKEN as TOKEN
from tests.smoke.cms_api_helpers import status_error


@pytest.mark.sso_api
@pytest.mark.session_auth
@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('sso-api:healthcheck'),
    get_absolute_url('sso-api:healthcheck-ping'),
])
def test_sso_api_health_check(absolute_url):
    """This endpoint still uses session auth"""
    params = {'token': TOKEN}
    response = requests.get(absolute_url, params=params)
    assert response.status_code == OK


@pytest.mark.sso_api
def test_sso_api_health_check_ping_with_sso_api_client():
    """Use SSO-API client"""
    response = sso_api_client.ping()
    assert response.status_code == OK


@pytest.mark.fab
@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('ui-buyer:healthcheck'),
])
def test_fab_health_check_endpoints(absolute_url, basic_auth):
    params = {'token': TOKEN}
    response = requests.get(absolute_url, params=params, auth=basic_auth)
    assert response.status_code == OK


@pytest.mark.fab
@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('ui-buyer:healthcheck'),
])
def test_fab_redirects_for_health_check_endpoints(absolute_url, basic_auth):
    params = {'token': TOKEN}
    # get rid of trailing slash
    absolute_url = absolute_url[:-1]
    response = requests.get(
        absolute_url, params=params, allow_redirects=False,
        auth=basic_auth)
    assert response.status_code == MOVED_PERMANENTLY


@pytest.mark.fab
@retry(
    wait_fixed=30000,
    stop_max_attempt_number=2,
    retry_on_exception=retriable_error,
)
@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('ui-buyer:healthcheck'),
])
def test_fab_302_redirects_after_removing_trailing_slash_for_anon_user(
        absolute_url, basic_auth):
    # get rid of trailing slash
    absolute_url = absolute_url[:-1]
    response = requests.get(
        absolute_url, allow_redirects=False, auth=basic_auth
    )
    assert response.status_code == MOVED_PERMANENTLY


@pytest.mark.fas
@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('ui-supplier:healthcheck'),
])
def test_fas_health_check_endpoints(absolute_url):
    params = {'token': TOKEN}
    response = requests.get(absolute_url, params=params)
    assert response.status_code == OK


@pytest.mark.invest
@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('ui-invest:healthcheck'),
])
def test_invest_health_check_endpoints(absolute_url):
    params = {'token': TOKEN}
    response = requests.get(absolute_url, params=params)
    assert response.status_code == OK


@pytest.mark.dir_api
@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('api:healthcheck'),
    get_absolute_url('api:healthcheck-ping'),
])
def test_dir_api_health_check_endpoints(absolute_url):
    params = {'token': TOKEN}
    response = requests.get(absolute_url, params=params)
    error = (f"Expected 200 OK from {absolute_url} but got "
             f"{response.status_code}. Check the reponse content: "
             f"{str(response.content)}")
    assert response.status_code == OK, error


@pytest.mark.profile
@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('profile:healthcheck'),
    get_absolute_url('profile:healthcheck-ping'),
])
def test_profile_health_check_endpoints_with_token(absolute_url):
    params = {'token': TOKEN}
    response = requests.get(absolute_url, params=params)
    assert response.status_code == OK


@pytest.mark.exred
@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('ui-exred:healthcheck'),
    get_absolute_url('ui-exred:healthcheck-ping'),
])
def test_exred_health_check_endpoints(absolute_url):
    params = {'token': TOKEN}
    response = requests.get(absolute_url, params=params)
    assert response.status_code == OK


@pytest.mark.cms
def test_cms_health_check_ping_endpoint_with_cms_api_client():
    endpoint = get_relative_url("cms-api:healthcheck-ping")
    response = cms_api_client.get(endpoint)
    assert response.status_code == OK, status_error(OK, response)


@pytest.mark.cms
@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('cms-api:healthcheck'),
    get_absolute_url('cms-api:healthcheck-ping'),
])
def test_cms_health_check_database_endpoint(absolute_url):
    params = {"token": TOKEN}
    response = requests.get(absolute_url, params=params)
    assert response.status_code == OK, status_error(OK, response)
