# -*- coding: utf-8 -*-
"""Profile - 'Find a Buyer' page"""
import logging

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.features.utils import Method, check_response, make_request

URL = get_absolute_url("profile:fab")
EXPECTED_STRINGS = [
    "Profile", "You are signed in as", "Export opportunities", "Find a buyer",
    "Selling online overseas", "About", "Sign out", "Reset password"
]

EXPECTED_STRINGS_WITH_PROFILE = [
    "Edit profile", "Add case study", "Edit logo"
]

EXPECTED_STRINGS_NO_PROFILE = [
    "Get a trade profile", "Create a trade profile",
    "Get a trade profile for your company and you can:",
    "generate new sales leads",
    "promote your business to thousands of overseas buyers",
    "add case studies of your best work to make your company stand out",
    "have buyers contact your sales team directly to get deals moving"
]


def go_to(session: Session) -> Response:
    """Go to the Profile 'Find a buyer' page / tab.

    :param session: Supplier session object
    :return: response object
    """
    headers = {"Referer": get_absolute_url("profile:about")}
    response = make_request(Method.GET, URL, session=session, headers=headers)
    should_be_here(response)
    logging.debug("Supplier is on the Profile 'Find a Buyer' page")
    return response


def should_be_here(response: Response):
    """Check if Supplier is on Profile 'Find a Buyer' page.

    NOTE:
    Supplier has to be logged in to get to this page.

    :param response: response object
    """
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the Profile 'Find a Buyer' page")


def should_see_get_a_trade_profile(response: Response):
    """Check if Supplier is on Profile 'Find a Buyer' page and can see
    a 'Get a trade profile' banner.

    NOTE:
    Supplier has to be logged in to get to this page.

    :param response: response object
    """
    expected = EXPECTED_STRINGS + EXPECTED_STRINGS_NO_PROFILE
    check_response(response, 200, body_contains=expected)
    logging.debug("Supplier can see 'Get a trade profile' banner")


def should_see_links_to_manage_trade_profile(response: Response):
    """Check if Supplier is on Profile 'Find a Buyer' page & can see links to
    manage company's trade profile.

    NOTE:
    Supplier has to be logged in to get to this page.

    :param response: response object
    """
    expected = EXPECTED_STRINGS + EXPECTED_STRINGS_WITH_PROFILE
    check_response(response, 200, body_contains=expected)
    logging.debug("Supplier can see links to manage the Trade Profile")


def go_to_create_a_trade_profile(session: Session) -> Response:
    """Go to the FAB Landing page.

    NOTE:
    This simulates a 'Click' on the 'Create a trade profile' button.

    :param session: Supplier session object
    :return: response object
    """
    url = get_absolute_url("ui-buyer:landing")
    response = make_request(Method.GET, url, session=session)
    return response
