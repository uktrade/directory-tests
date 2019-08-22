from urllib.parse import urljoin

import pytest
from rest_framework.status import HTTP_200_OK

from tests import URLs
from tests.smoke.cms_api_helpers import get_and_assert


@pytest.mark.parametrize(
    "url",
    [
        urljoin(URLs.DOMESTIC_LANDING.absolute, "robots.txt"),
        urljoin(URLs.EXOPPS_LANDING.absolute, "robots.txt"),
        urljoin(URLs.FAB_LANDING.absolute, "robots.txt"),
        urljoin(URLs.INTERNATIONAL_LANDING.absolute, "robots.txt"),
        # urljoin(URLs.PROFILE_LANDING.absolute, "robots.txt"), see TT-1499
        urljoin(URLs.SOO_LANDING.absolute, "robots.txt"),
        urljoin(URLs.SSO_LANDING.absolute, "robots.txt"),
    ],
)
def test_robots_txt(url, basic_auth):
    get_and_assert(
        url=url, status_code=HTTP_200_OK, auth=basic_auth
    )
