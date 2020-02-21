# -*- coding: utf-8 -*-
import pytest
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_301_MOVED_PERMANENTLY,
    HTTP_404_NOT_FOUND,
)
from retrying import retry

import allure
from directory_tests_shared import URLs
from directory_tests_shared.clients import (
    BASIC_AUTHENTICATOR,
    CMS_API_CLIENT,
    SSO_API_CLIENT,
)
from directory_tests_shared.settings import DIRECTORY_API_HEALTH_CHECK_TOKEN as TOKEN
from directory_tests_shared.utils import retriable_error
from tests.smoke.cms_api_helpers import get_and_assert, status_error

pytestmark = [allure.suite("Health checks"), allure.feature("Health checks")]


@pytest.mark.sso_api
@pytest.mark.parametrize(
    "url", [URLs.SSO_API_HEALTHCECK.absolute, URLs.SSO_API_HEALTHCHECK_PING.absolute]
)
def test_sso_api_health_check(url, basic_auth):
    """This endpoint still uses session auth"""
    params = {"token": TOKEN}
    get_and_assert(url=url, params=params, status_code=HTTP_200_OK, auth=basic_auth)


@pytest.mark.sso_api
def test_sso_api_health_check_ping_with_sso_api_client():
    """Use SSO-API client"""
    response = SSO_API_CLIENT.ping(authenticator=BASIC_AUTHENTICATOR)
    assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)
    assert "Access Denied" not in response.content.decode("UTF-8")


@pytest.mark.fab
@pytest.mark.parametrize("url", [URLs.FAB_HEALTHCHECK.absolute])
def test_fab_health_check_endpoints(url, basic_auth):
    params = {"token": TOKEN}
    get_and_assert(url=url, params=params, status_code=HTTP_200_OK, auth=basic_auth)


@pytest.mark.fab
@pytest.mark.parametrize("url", [URLs.FAB_HEALTHCHECK.absolute])
def test_fab_redirects_for_health_check_endpoints(url, basic_auth):
    params = {"token": TOKEN}
    # get rid of trailing slash
    if url[-1] == "/":
        url = url[:-1]
    get_and_assert(
        url=url,
        params=params,
        allow_redirects=False,
        status_code=HTTP_301_MOVED_PERMANENTLY,
        auth=basic_auth,
    )


@pytest.mark.fab
@retry(wait_fixed=30000, stop_max_attempt_number=2, retry_on_exception=retriable_error)
@pytest.mark.parametrize("url", [URLs.FAB_HEALTHCHECK.absolute])
def test_fab_302_redirects_after_removing_trailing_slash_for_anon_user(url, basic_auth):
    # get rid of trailing slash
    if url[-1] == "/":
        url = url[:-1]
    get_and_assert(
        url=url,
        allow_redirects=False,
        status_code=HTTP_301_MOVED_PERMANENTLY,
        auth=basic_auth,
    )


@pytest.mark.fas
@pytest.mark.parametrize("url", [URLs.FAS_HEALTHCHECK.absolute])
def test_fas_health_check_endpoints(url, basic_auth):
    params = {"token": TOKEN}
    get_and_assert(
        url=url, params=params, status_code=HTTP_404_NOT_FOUND, auth=basic_auth
    )


@pytest.mark.dir_api
@pytest.mark.parametrize(
    "url", [URLs.DIR_API_HEALTHCHECK.absolute, URLs.DIR_API_HEALTHCHECK_PING.absolute]
)
def test_dir_api_health_check_endpoints(url, basic_auth):
    params = {"token": TOKEN}
    get_and_assert(url=url, params=params, status_code=HTTP_200_OK, auth=basic_auth)


@pytest.mark.profile
@pytest.mark.parametrize(
    "url", [URLs.PROFILE_HEALTHCHECK.absolute, URLs.PROFILE_HEALTHCHECK_PING.absolute]
)
def test_profile_health_check_endpoints_with_token(url, basic_auth):
    params = {"token": TOKEN}
    get_and_assert(url=url, params=params, status_code=HTTP_200_OK, auth=basic_auth)


@pytest.mark.exred
@pytest.mark.parametrize(
    "url",
    [
        # See bug TT-1805
        # URLs.DOMESTIC_HEALTHCHECK.absolute,
        URLs.DOMESTIC_HEALTHCHECK_PING.absolute
    ],
)
def test_exred_health_check_endpoints(url, basic_auth):
    params = {"token": TOKEN}
    get_and_assert(url=url, params=params, status_code=HTTP_200_OK, auth=basic_auth)


@pytest.mark.cms
@pytest.mark.parametrize("endpoint", [URLs.CMS_API_HEALTHCHECK_PING.relative])
def test_cms_health_check_ping_endpoint_with_cms_api_client(endpoint):
    response = CMS_API_CLIENT.get(endpoint)
    assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)


@pytest.mark.cms
@pytest.mark.parametrize(
    "url", [URLs.CMS_API_HEALTHCHECK.absolute, URLs.CMS_API_HEALTHCHECK_PING.absolute]
)
def test_cms_health_check_database_endpoint(url, basic_auth):
    params = {"token": TOKEN}
    get_and_assert(url=url, params=params, status_code=HTTP_200_OK, auth=basic_auth)


@pytest.mark.forms
@pytest.mark.parametrize(
    "url",
    [URLs.FORMS_API_HEALTHCHECK.absolute, URLs.FORMS_API_HEALTHCHECK_PING.absolute],
)
def test_forms_healthcheck_endpoint(url, basic_auth):
    params = {"token": TOKEN}
    get_and_assert(url=url, params=params, status_code=HTTP_200_OK, auth=basic_auth)


@pytest.mark.international
@pytest.mark.parametrize(
    "url",
    [
        URLs.INTERNATIONAL_HEALTHCHECK_FORMS_API.absolute,
        URLs.INTERNATIONAL_HEALTHCHECK_SENTRY.absolute,
    ],
)
def test_international_healthcheck_endpoint(url, basic_auth):
    params = {"token": TOKEN}
    get_and_assert(url=url, params=params, status_code=HTTP_200_OK, auth=basic_auth)
