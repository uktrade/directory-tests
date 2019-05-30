from urllib.parse import urljoin

import pytest
from rest_framework.status import HTTP_200_OK

from tests import get_absolute_url
from tests.smoke.cms_api_helpers import get_and_assert


@pytest.mark.parametrize(
    "url",
    [
        # urljoin(get_absolute_url("profile:landing"), "robots.txt"),see TT-1499
        urljoin(get_absolute_url("sso:landing"), "robots.txt"),
        urljoin(get_absolute_url("ui-buyer:landing"), "robots.txt"),
        urljoin(get_absolute_url("ui-exopps:landing"), "robots.txt"),
        urljoin(get_absolute_url("ui-exred:landing"), "robots.txt"),
        urljoin(get_absolute_url("ui-international:landing"), "robots.txt"),
        urljoin(get_absolute_url("ui-invest:landing"), "robots.txt"),
        urljoin(get_absolute_url("ui-soo:landing"), "robots.txt"),
        urljoin(get_absolute_url("ui-supplier:landing"), "robots.txt"),
    ],
)
def test_robots_txt(url, basic_auth):
    get_and_assert(
        url=url, status_code=HTTP_200_OK, auth=basic_auth
    )
