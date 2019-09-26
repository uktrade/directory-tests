# -*- coding: utf-8 -*-
"""Profile - Business profile"""
import logging

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.generic import assertion_msg
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Service.PROFILE
NAME = "Business Profile"
TYPE = PageType.LANDING
URL = URLs.PROFILE_BUSINESS_PROFILE.absolute
EXPECTED_STRINGS = [
    "Account",
    "You are signed in as",
    "Export opportunities",
    "Business profile",
    "Selling online overseas",
    "Add a case study",
    "Add a logo",
]

MANAGE_USER_ACCOUNTS_STRINGS = ["Admin tools"]

EXPECTED_STRINGS_USER_ADDED = [
    "We’ve emailed the person you want to add to this account"
]
EXPECTED_STRINGS_OWNER_TRANSFERRED = [
    "We’ve sent a confirmation email to the new profile owner."
]
EXPECTED_STRINGS_USER_REMOVED = ["User successfully removed from your profile"]


def go_to(session: Session) -> Response:
    headers = {"Referer": URLs.PROFILE_ABOUT.absolute}
    return make_request(Method.GET, URL, session=session, headers=headers)


def should_be_here(
    response: Response,
    *,
    user_added: bool = False,
    owner_transferred: bool = False,
    user_removed: bool = False,
):
    """Check if Supplier is on Profile 'Find a Buyer' page.

    NOTE:
    Supplier has to be logged in to get to this page.
    """
    check_response(response, 200, body_contains=EXPECTED_STRINGS)

    expected_query = None
    expected_strings = None
    if user_added:
        expected_query = "?user-added"
        expected_strings = EXPECTED_STRINGS_USER_ADDED
    if owner_transferred:
        expected_query = "?owner-transferred"
        expected_strings = EXPECTED_STRINGS_OWNER_TRANSFERRED
    if user_removed:
        expected_query = "?user-removed"
        expected_strings = EXPECTED_STRINGS_USER_REMOVED

    if expected_strings:
        error = (
            f"Expected to see '{expected_query}' in the URL but got: "
            f"'{response.url}' instead"
        )
        with assertion_msg(error):
            assert expected_query in response.url
        check_response(response, 200, body_contains=expected_strings)

    logging.debug("Successfully got to the Profile 'Find a Buyer' page")


def should_see_options_to_manage_users(response: Response):
    check_response(response, 200, body_contains=MANAGE_USER_ACCOUNTS_STRINGS)
    logging.debug("User can see options to control FAB profile user accounts")


def should_not_see_options_to_manage_users(response: Response):
    check_response(response, 200, unexpected_strings=MANAGE_USER_ACCOUNTS_STRINGS)
    logging.debug("User can't see options to manage FAB profile user accounts")
