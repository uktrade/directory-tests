# -*- coding: utf-8 -*-
"""Profile - Start Individual enrolment"""

from requests import Response

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.request import check_response, check_url

SERVICE = Service.PROFILE
NAME = "Individual enrolment (start)"
TYPE = PageType.CONFIRMATION
URL = URLs.PROFILE_ENROL_INDIVIDUAL_START.absolute
EXPECTED_STRINGS = [
    "You cannot update your details",
    "Continue creating account for individual",
]


def should_be_here(response: Response):
    check_url(response, URL)
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
