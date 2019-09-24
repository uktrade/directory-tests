# -*- coding: utf-8 -*-
"""Find a Buyer - Confirm Identity page"""
import logging
from copy import copy

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Service.FAB
NAME = "Confirm identity"
TYPE = PageType.OPTION
URL = URLs.FAB_CONFIRM_IDENTITY.absolute
EXPECTED_STRINGS = [
    "Confirm your identity",
    "For security, we need to check you’re who you say you are.",
    (
        "You can sign in with Companies House to confirm your identity straight "
        "away. You’ll need your Companies House username and password."
    ),
    (
        "Alternatively, we can send a confirmation letter to your company’s "
        "registered address."
    ),
    "Sign in with Companies House",
    (
        "Enter your Companies House username and password. We’ll be able to "
        "confirm your identity instantly."
    ),
    "Sign in",
    "Get confirmation letter",
    "Back",
    (
        "We’ll then send a confirmation letter to your company’s registered "
        "address within 5 working days. If you can’t collect the letter "
        "yourself, you’ll need to make sure someone can send it on to you"
    ),
]

EXPECTED_STRINGS_DURING_PROFILE_BUILDING = ["Send"]

EXPECTED_STRINGS_WHILE_LETTER_VERIFICATION = ["Verify with your address"]


def go_to(session: Session):
    response = make_request(Method.GET, URL, session=session)
    return response


def should_be_here(
    response: Response,
    *,
    profile_building: bool = False,
    letter_verification: bool = False
):
    """Check if Supplier is on FAB Confirm your Identity page.

    :param profile_building: (optional) if True, then it will look for specific
                             strings displayed when building company's profile
    :param letter_verification: (optional) if True, then it will look for
                                specific strings displayed when verifying the
                                identity with a code from a letter
    :param response: response object
    """
    expected = copy(EXPECTED_STRINGS)
    if profile_building:
        expected += EXPECTED_STRINGS_DURING_PROFILE_BUILDING
    if letter_verification:
        expected += EXPECTED_STRINGS_WHILE_LETTER_VERIFICATION
    check_response(response, 200, body_contains=expected)
    logging.debug("Successfully got to the FAB Confirm your Identity page")
