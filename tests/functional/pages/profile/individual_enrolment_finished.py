# -*- coding: utf-8 -*-
"""Profile - Individual enrolment finished"""

from requests import Response

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.request import check_response, check_url

SERVICE = Service.PROFILE
NAME = "Individual enrolment (finished)"
TYPE = PageType.CONFIRMATION
URL = URLs.PROFILE_ENROL_INDIVIDUAL_FINISHED.absolute
EXPECTED_STRINGS = [
    "Your account has been created",
    "What you can do next",
    "find the right digital marketplace",
    "apply to take part in events",
]


def should_be_here(response: Response):
    check_url(response, URL)
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
