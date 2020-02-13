# -*- coding: utf-8 -*-
import pytest
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
)

import allure
from directory_tests_shared import URLs
from directory_tests_shared.clients import FORMS_API_CLIENT
from tests.smoke.cms_api_helpers import status_error

pytestmark = [allure.suite("Forms-API"), allure.feature("Forms-API")]


@pytest.mark.forms
def test_forms_submissions_endpoint_accepts_only_post():
    response = FORMS_API_CLIENT.get(URLs.FORMS_API_SUBMISSION.absolute)
    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED, status_error(
        HTTP_405_METHOD_NOT_ALLOWED, response
    )
    assert response.headers["Allow"] == "POST, OPTIONS"


@pytest.mark.forms
def test_forms_admin_is_available():
    response = FORMS_API_CLIENT.get(URLs.FORMS_API_ADMIN.absolute)
    assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)


@pytest.mark.dev
@pytest.mark.forms
@pytest.mark.parametrize("email", ["asdf@sdf.pl"])
def test_forms_testapi_endpoint_is_present_on_dev(email: str):
    response = FORMS_API_CLIENT.get(URLs.FORMS_API_TESTAPI.absolute.format(email=email))
    assert response.status_code == HTTP_200_OK, status_error(HTTP_200_OK, response)


@pytest.mark.stage
@pytest.mark.forms
@pytest.mark.parametrize("email", ["test@gmail.com"])
def test_forms_testapi_endpoint_is_present_on_stage(email):
    test_forms_testapi_endpoint_is_present_on_dev(email)


@pytest.mark.prod
@pytest.mark.forms
def test_forms_testapi_endpoints_are_not_present_on_prod():
    response = FORMS_API_CLIENT.get(URLs.FORMS_API_TESTAPI.absolute)
    assert response.status_code == HTTP_404_NOT_FOUND, status_error(
        HTTP_404_NOT_FOUND, response
    )
