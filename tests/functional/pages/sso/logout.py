# -*- coding: utf-8 -*-
"""SSO - Logout page"""
import logging
from urllib.parse import urljoin

from requests import Response, Session

from tests import URLs
from tests.functional.pages import Services
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Services.SSO
NAME = "Logout"
TYPE = "form"
URL = URLs.SSO_LOGOUT.absolute
EXPECTED_STRINGS = ["Sign out", "Are you sure you want to sign out?"]


def go_to(session: Session, *, next_param: str = None) -> Response:
    fab_landing = URLs.FAB_LANDING.absolute
    params = {"next": next_param or fab_landing}
    headers = {"Referer": URLs.PROFILE_FAB.absolute}
    return make_request(
        Method.GET, URL, session=session, params=params, headers=headers
    )


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the SSO logout page")


def logout(
    session: Session, token: str, *, next_param: str = None
) -> Response:
    fab_landing = URLs.FAB_LANDING.absolute
    data = {"csrfmiddlewaretoken": token, "next": next_param or fab_landing}
    query = f"?next={fab_landing}"
    headers = {"Referer": urljoin(URL, query)}
    return make_request(
        Method.POST, URL, session=session, headers=headers, data=data
    )
