# -*- coding: utf-8 -*-
import pytest
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
)

import allure
from directory_tests_shared import URLs
from directory_tests_shared.clients import FORMS_API_CLIENT, BasicAuthenticator
from directory_tests_shared.settings import BASICAUTH_PASS, BASICAUTH_USER
from tests.smoke.cms_api_helpers import status_error

pytestmark = [allure.suite("Forms-API"), allure.feature("Forms-API")]

BASIC_AUTHENTICATOR = BasicAuthenticator(BASICAUTH_USER, BASICAUTH_PASS)


@pytest.mark.forms
def test_forms_submissions_endpoint_accepts_only_post():
    response = FORMS_API_CLIENT.get(
        URLs.FORMS_API_SUBMISSION.absolute, authenticator=BASIC_AUTHENTICATOR
    )
    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED, status_error(
        HTTP_405_METHOD_NOT_ALLOWED, response
    )
    assert response.headers["Allow"] == "POST, OPTIONS"


@pytest.mark.forms
def test_forms_admin_is_not_available_for_unauthenticated_requests():
    response = FORMS_API_CLIENT.get(URLs.FORMS_API_ADMIN.absolute)
    assert response.status_code == HTTP_403_FORBIDDEN, status_error(
        HTTP_403_FORBIDDEN, response
    )


@pytest.mark.forms
def test_forms_admin_is_available_for_authenticated_requests():
    response = FORMS_API_CLIENT.get(
        URLs.FORMS_API_ADMIN.absolute, authenticator=BASIC_AUTHENTICATOR
    )
    assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)


@pytest.mark.dev
@pytest.mark.forms
@pytest.mark.parametrize("email", ["asdf@sdf.pl"])
def test_forms_testapi_endpoint_is_present_on_dev(email: str):
    response = FORMS_API_CLIENT.get(
        URLs.FORMS_API_TESTAPI.absolute.format(email=email),
        authenticator=BASIC_AUTHENTICATOR,
    )
    assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)


@pytest.mark.stage
@pytest.mark.forms
@pytest.mark.parametrize("email", ["test@gmail.com"])
def test_forms_testapi_endpoint_is_present_on_stage(email):
    test_forms_testapi_endpoint_is_present_on_dev(email)


@pytest.mark.prod
@pytest.mark.forms
def test_forms_testapi_endpoints_are_not_present_on_prod():
    response = FORMS_API_CLIENT.get(
        URLs.FORMS_API_TESTAPI.absolute, authenticator=BASIC_AUTHENTICATOR
    )
    assert response.status_code == HTTP_404_NOT_FOUND, status_error(
        HTTP_404_NOT_FOUND, response
    )
