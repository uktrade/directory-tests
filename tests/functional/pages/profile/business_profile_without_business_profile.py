# -*- coding: utf-8 -*-
"""Profile - Business profile (without a profile)"""
import logging

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Service.PROFILE
NAME = "Business Profile (without a business profile)"
TYPE = PageType.LANDING
URL = URLs.PROFILE_BUSINESS_PROFILE.absolute
EXPECTED_STRINGS = [
    "Account",
    "You are signed in as",
    "Get a business profile",
    "Get a business profile for your company and you can",
    "Create a business profile",
]


def go_to(session: Session) -> Response:
    headers = {"Referer": URLs.PROFILE_ABOUT.absolute}
    return make_request(Method.GET, URL, session=session, headers=headers)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the Profile 'Find a Buyer' page")
