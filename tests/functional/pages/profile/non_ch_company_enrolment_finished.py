# -*- coding: utf-8 -*-
"""Profile - Non Companies House company enrolment finished"""

from requests import Response

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.request import check_response, check_url

SERVICE = Service.PROFILE
NAME = "Enrolment (finished)"
TYPE = PageType.CONFIRMATION
URL = URLs.PROFILE_ENROL_NON_CH_COMPANY_FINISHED.absolute
EXPECTED_STRINGS = [
    "Account created",
    "Your account has been created",
    "Next steps",
    "You can now",
    "publish your business profile",
    "find export opportunities",
    "sell online overseas",
    "find events and visits",
]


def should_be_here(response: Response):
    check_url(response, URL)
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
