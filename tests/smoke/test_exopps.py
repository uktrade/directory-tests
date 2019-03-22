import pytest
from rest_framework.status import HTTP_200_OK

from tests import get_absolute_url
from tests.smoke.cms_api_helpers import get_and_assert


@pytest.mark.stage
@pytest.mark.parametrize(
    "url",
    [
        get_absolute_url("ui-exopps:landing"),
    ],
)
def test_exops_pages(url, basic_auth):
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)
