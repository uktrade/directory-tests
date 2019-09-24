# -*- coding: utf-8 -*-
"""Find a Buyer - Landing page"""
import logging

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.generic import assertion_msg
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Service.FAB
NAME = "Landing"
TYPE = PageType.LANDING
URL = URLs.FAB_LANDING.absolute
EXPECTED_STRINGS = [
    "Connect directly with international buyers",
    "Create a business profile on great.gov.uk.",
    "Start now",
]


def go_to(session: Session) -> Response:
    return make_request(Method.GET, URL, session=session)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the FAB Landing page")


def should_be_logged_out(response: Response):
    """Check if Supplier is logged out by checking the cookies."""
    with assertion_msg(
        "Found sso_display_logged_in cookie in the response. Maybe user is"
        " still logged in?"
    ):
        assert "sso_display_logged_in" not in response.cookies
    with assertion_msg(
        "Found directory_sso_dev_session cookie in the response. Maybe "
        "user is still logged in?"
    ):
        assert "directory_sso_dev_session" not in response.cookies
