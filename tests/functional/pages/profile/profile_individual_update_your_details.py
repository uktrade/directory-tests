# -*- coding: utf-8 -*-
"""Profile - Enrol - update your details"""

from requests import Response

from tests import URLs
from tests.functional.pages import Services
from tests.functional.utils.request import check_response, check_url

SERVICE = Services.PROFILE
NAME = "Update your details"
TYPE = "landing"
URL = URLs.PROFILE_ENROL_INDIVIDUAL_UPDATE_YOUR_DETAILS.absolute
EXPECTED_STRINGS = [
    "Update your details",
    "Select your business type",
    "Enter your business details",
    "Enter your details",
    "Start now",
]


def should_be_here(response: Response):
    check_url(response, URL)
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
