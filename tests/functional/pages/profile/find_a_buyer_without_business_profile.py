# -*- coding: utf-8 -*-
"""SSO - SUD (Profile) Find A Buyer page"""
import logging

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs

from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Service.PROFILE
NAME = "Find a Buyer (without a business profile)"
TYPE = PageType.LANDING
URL = URLs.PROFILE_FAB.absolute
EXPECTED_STRINGS = [
    'Account',
    'You are signed in as',
    'Get a business profile',
    'Get a business profile for your company and you can',
    'generate new sales leads',
    'promote your business to thousands of overseas buyers',
    'add case studies of your best work to make your company stand out',
    'have buyers contact your sales team directly to get deals moving',
    'Create a business profile',
]


def go_to(session: Session) -> Response:
    headers = {"Referer": URLs.PROFILE_ABOUT.absolute}
    return make_request(Method.GET, URL, session=session, headers=headers)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the Profile 'Find a Buyer' page")
