import pytest
from rest_framework.status import *

from directory_tests_shared import URLs
from tests.smoke.cms_api_helpers import get_and_assert


@pytest.mark.dev
@pytest.mark.parametrize(
    "url",
    [
        URLs.INTERNATIONAL_REGIONS_MIDLANDS.absolute,
        URLs.INTERNATIONAL_REGIONS_NORTH_ENGLAND.absolute,
        URLs.INTERNATIONAL_REGIONS_NORTHERN_IRELAND.absolute,
        URLs.INTERNATIONAL_REGIONS_SOUTH_ENGLAND.absolute,
        URLs.INTERNATIONAL_REGIONS_WALES.absolute,
    ],
)
def test_region_pages(url, basic_auth):
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth, allow_redirects=True)

