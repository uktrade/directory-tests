# -*- coding: utf-8 -*-
"""SSO - Verify your email page"""
import logging
from urllib.parse import urljoin

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.context_utils import Actor
from tests.functional.utils.generic import assertion_msg
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Service.SSO
NAME = "Password reset"
TYPE = PageType.FORM
URL = URLs.SSO_PASSWORD_RESET.absolute
EXPECTED_STRINGS = [
    "Password reset",
    "Enter the email address you used to register",
    "Email",
    "Reset my password",
    "Contact us",
    "if the password reset doesn't work.",
]

EXPECTED_STRINGS_PASSWORD_RESET = [
    "Password reset email",
    ("We've sent a password reset email. Click on the link to reset your " "password"),
    "Contact us",
    "if you haven't received the email within 10 minutes",
]


def go_to(session: Session, *, next_param: str = None) -> Response:
    fab_landing = URLs.FAB_LANDING.absolute
    params = {"next": next_param or fab_landing}
    headers = {"Referer": fab_landing}
    return make_request(
        Method.GET, URL, session=session, params=params, headers=headers
    )


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the SSO Password Reset page")


def should_see_that_password_was_reset(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS_PASSWORD_RESET)
    logging.debug("Successfully Reset Password")


def reset(
    actor: Actor, token: str, *, referer: str = None, next_param: str = None
) -> Response:
    session = actor.session
    fab_landing = URLs.FAB_LANDING.absolute

    data = {
        "next": next_param or fab_landing,
        "csrfmiddlewaretoken": token,
        "email": actor.email,
    }
    # Referer is the same as the final URL from the previous request
    query = f"?next={next_param or fab_landing}"
    referer = referer or urljoin(URL, query)
    headers = {"Referer": referer}

    return make_request(Method.POST, URL, session=session, data=data, headers=headers)


def open_link(session: Session, link: str) -> Response:
    with assertion_msg("Expected a non-empty password reset email link"):
        assert link
    return make_request(Method.GET, link, session=session)
