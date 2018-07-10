# -*- coding: utf-8 -*-
"""SSO - SUD (Profile) About page"""
import logging

from requests import Response, Session
from tests import get_absolute_url
from tests.functional.utils.request import Method, check_response, make_request

URL = get_absolute_url("profile:about")
EXPECTED_STRINGS = [
    "Profile",
    "Welcome to your great.gov.uk profile",
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
    logging.debug("Successfully got to the SUD (Profile) About page")
