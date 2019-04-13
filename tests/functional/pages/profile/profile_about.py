# -*- coding: utf-8 -*-
"""Profile - About page"""
import logging

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.pages import Services
from tests.functional.utils.generic import assertion_msg
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Services.PROFILE
NAME = "About"
TYPE = "landing"
URL = get_absolute_url("profile:about")
EXPECTED_STRINGS = [
    "Account",
    "Welcome to your great.gov.uk account",
    (
        "From now on, every time you sign in you’ll be able to quickly access all"
        " of our exporting tools in one place. The tools are here to help your "
        "business succeed internationally."
    ),
]


def go_to(session: Session, *, set_next_page: bool = True) -> Response:
    fab_landing = get_absolute_url("ui-buyer:landing")
    params = {"next": fab_landing}
    headers = {"Referer": fab_landing}
    if not set_next_page:
        params = None
    return make_request(
        Method.GET, URL, session=session, params=params, headers=headers
    )


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the Profile About page")


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
