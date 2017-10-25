# -*- coding: utf-8 -*-
"""FAB - Landing page"""
import logging

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.utils.generic import assertion_msg
from tests.functional.utils.request import Method, check_response, make_request

URL = get_absolute_url("ui-buyer:landing")
EXPECTED_STRINGS = [
    "Find a Buyer - GREAT.gov.uk", "Get promoted internationally",
    "with a great.gov.uk trade profile",
    "Enter your Companies House number"
]


def go_to(session: Session) -> Response:
    """Go to the FAB Landing page.

    :param session: Supplier session object
    :return: response object
    """
    response = make_request(Method.GET, URL, session=session)
    return response


def should_be_here(response: Response):
    """Check if Supplier is on FAB Landing page

    :param response: response object
    """
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the FAB Landing page")


def should_be_logged_out(response: Response):
    """Check if Supplier is logged out by checking the cookies.

    :param response: response object
    """
    with assertion_msg(
            "Found sso_display_logged_in cookie in the response. Maybe user is"
            " still logged in?"):
        assert "sso_display_logged_in" not in response.cookies
    with assertion_msg(
            "Found directory_sso_dev_session cookie in the response. Maybe "
            "user is still logged in?"):
        assert "directory_sso_dev_session" not in response.cookies
