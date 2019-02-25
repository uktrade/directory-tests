import pytest
from rest_framework.status import *

from directory_client_core.base import AbstractAPIClient

from tests import get_absolute_url, settings
from tests.smoke.cms_api_helpers import status_error


class FormsClient(AbstractAPIClient):
    version = "1"

    def __init__(
            self, base_url, api_key, sender_id, timeout, default_service_name,
    ):
        super().__init__(base_url, api_key, sender_id, timeout)
        self.default_service_name = default_service_name


client = FormsClient(
    base_url=settings.DIRECTORY_FORMS_API_URL,
    api_key=settings.DIRECTORY_FORMS_API_KEY,
    sender_id=settings.DIRECTORY_FORMS_API_SENDER_ID,
    timeout=30,
    default_service_name="testapi"
)


@pytest.mark.forms
def test_forms_submissions_endpoint_accepts_only_post():
    response = client.get(get_absolute_url("forms-api:submission"))
    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED, status_error(
        HTTP_405_METHOD_NOT_ALLOWED, response
    )
    assert response.headers["Allow"] == "POST, OPTIONS"


@pytest.mark.forms
def test_forms_admin_is_available():
    response = client.get(get_absolute_url("forms-api:admin"))
    assert response.status_code == HTTP_200_OK, status_error(
        HTTP_200_OK, response
    )


@pytest.mark.dev
@pytest.mark.forms
def test_forms_testapi_endpoint_is_present_on_dev():
    response = client.get(
        get_absolute_url("forms-api:testapi").format(email="test@example.com")
    )
    assert response.status_code == HTTP_200_OK, status_error(
        HTTP_200_OK, response
    )


@pytest.mark.stage
@pytest.mark.forms
def test_forms_testapi_endpoint_is_present_on_stage():
    test_forms_testapi_endpoint_is_present_on_dev()


@pytest.mark.prod
@pytest.mark.forms
def test_forms_testapi_endpoints_are_not_present_on_prod():
    response = client.get(get_absolute_url("forms-api:testapi"))
    assert response.status_code == HTTP_404_NOT_FOUND, status_error(
        HTTP_404_NOT_FOUND, response
    )
