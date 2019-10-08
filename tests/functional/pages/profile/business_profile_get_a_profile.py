# -*- coding: utf-8 -*-
"""Profile - Business profile page seen by a user without a business profile"""
import logging

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.request import (
    Method,
    check_response,
    check_url,
    make_request,
)

SERVICE = Service.PROFILE
NAME = "Business Profile (get a profile)"
TYPE = PageType.LANDING
URL = URLs.PROFILE_BUSINESS_PROFILE.absolute
EXPECTED_STRINGS = [
    "Account",
    "You are signed in as",
    "Export opportunities",
    "Business profile",
    "Selling online overseas",
    "Get a business profile",
    "Get a business profile for your company and you can",
]
MANAGE_USER_ACCOUNTS_STRINGS = ["Admin tools"]


def go_to(session: Session) -> Response:
    headers = {"Referer": URLs.PROFILE_ABOUT.absolute}
    return make_request(Method.GET, URL, session=session, headers=headers)


def should_be_here(response: Response,):
    check_url(response, URL)
    check_response(response, 200, body_contains=EXPECTED_STRINGS)


def should_not_see_options_to_manage_users(response: Response):
    check_response(response, 200, unexpected_strings=MANAGE_USER_ACCOUNTS_STRINGS)
    logging.debug("User can't see options to manage FAB profile user accounts")
