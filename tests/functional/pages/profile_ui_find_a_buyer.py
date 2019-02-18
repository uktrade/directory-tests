# -*- coding: utf-8 -*-
"""Profile - 'Find a Buyer' page"""
import logging

from requests import Response, Session
from tests import get_absolute_url
from tests.functional.utils.generic import assertion_msg
from tests.functional.utils.request import Method, check_response, make_request

URL = get_absolute_url("profile:fab")
EXPECTED_STRINGS = [
    "Account",
    "You are signed in as",
    "Export opportunities",
    "Business profile",
    "Selling online overseas",
    "About",
    "Sign out",
    "Reset password",
]

EXPECTED_STRINGS_WITH_PROFILE = [
    "Edit profile",
    "Add case study",
    "Edit logo",
    "Account details",
    "Add user to account",
    "Remove user from account",
    "Transfer account",
]

EXPECTED_STRINGS_NO_PROFILE = [
    "Get a business profile",
    "Create a business profile",
    "Get a business profile for your company and you can:",
    "generate new sales leads",
    "promote your business to thousands of overseas buyers",
    "add case studies of your best work to make your company stand out",
    "have buyers contact your sales team directly to get deals moving",
]

EXPECTED_STRINGS_OWNER_TRANSFERRED = [
    "We’ve sent a confirmation email to the new profile owner."
]
EXPECTED_STRINGS_USER_ADDED = [
    "We’ve sent an invitation to the user you want added to your profile."
]
EXPECTED_STRINGS_USER_REMOVED = ["User successfully removed from your profile"]


def go_to(session: Session) -> Response:
    headers = {"Referer": get_absolute_url("profile:about")}
    return make_request(Method.GET, URL, session=session, headers=headers)


def should_be_here(
    response: Response,
    *,
    user_added: bool = False,
    owner_transferred: bool = False,
    user_removed: bool = False
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
        error = (f"Expected to see '{expected_query}' in the URL but got: "
                 f"'{response.url}' instead")
        with assertion_msg(error):
            assert expected_query in response.url
        check_response(response, 200, body_contains=expected_strings)

    logging.debug("Successfully got to the Profile 'Find a Buyer' page")


def should_see_get_a_trade_profile(response: Response):
    """Check if Supplier is on Profile 'Find a Buyer' page and can see
    a 'Get a trade profile' banner.

    NOTE:
    Supplier has to be logged in to get to this page.
    """
    expected = EXPECTED_STRINGS + EXPECTED_STRINGS_NO_PROFILE
    check_response(response, 200, body_contains=expected)
    logging.debug("Supplier can see 'Get a trade profile' banner")


def should_see_links_to_manage_trade_profile(response: Response):
    """Check if Supplier is on Profile 'Find a Buyer' page & can see links to
    manage company's trade profile.

    NOTE:
    Supplier has to be logged in to get to this page.
    """
    expected = EXPECTED_STRINGS + EXPECTED_STRINGS_WITH_PROFILE
    check_response(response, 200, body_contains=expected)
    logging.debug("Supplier can see links to manage the Trade Profile")


def go_to_create_a_trade_profile(session: Session) -> Response:
    """Go to the FAB Landing page.

    NOTE:
    This simulates a 'Click' on the 'Create a trade profile' button.
    """
    url = get_absolute_url("ui-buyer:landing")
    return make_request(Method.GET, url, session=session)
