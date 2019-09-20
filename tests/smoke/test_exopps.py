# -*- coding: utf-8 -*-
import pytest
from rest_framework.status import HTTP_200_OK

from directory_tests_shared import URLs
from tests.smoke.cms_api_helpers import get_and_assert


@pytest.mark.stage
@pytest.mark.parametrize(
    "url",
    [
        URLs.EXOPPS_LANDING.absolute,
    ],
)
def test_exops_pages(url, basic_auth):
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)
