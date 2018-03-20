# -*- coding: utf-8 -*-
"""SSO - Verify your email page"""
import logging
from urllib.parse import urljoin

from requests import Response, Session
from tests import get_absolute_url
from tests.functional.utils.context_utils import Actor
from tests.functional.utils.generic import assertion_msg
from tests.functional.utils.request import Method, check_response, make_request

URL = get_absolute_url("sso:password_reset")
EXPECTED_STRINGS = [
    "Password reset", "Enter the email address you used to register",
    "Email:", "Reset my password", "Contact us",
    "if the password reset doesn't work."
]

EXPECTED_STRINGS_PASSWORD_RESET = [
    "Password reset email",
    ("We've sent a password reset email. Click on the link to reset your "
     "password"),
    "Contact us", "if you haven't received the email within 10 minutes"
]


def go_to(session: Session, *, next_param: str = None) -> Response:
    fab_landing = get_absolute_url("ui-buyer:landing")
    params = {"next": next_param or fab_landing}
    headers = {"Referer": fab_landing}
    response = make_request(
        Method.GET, URL, session=session, params=params, headers=headers)
    return response


def should_be_here(response: Response):
    """Check if Supplier is on SSO Password Reset Page.

    :param response: response object
    """
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the SSO Password Reset page")


def should_see_that_password_was_reset(response: Response):
    """Check if Supplier is on SSO Password Reset confirmation Page.

    :param response: response object
    """
    check_response(response, 200, body_contains=EXPECTED_STRINGS_PASSWORD_RESET)
    logging.debug("Successfully Reset Password")


def reset(
        actor: Actor, token: str, *, referer: str = None,
        next_param: str = None) -> Response:
    """Try to reset the password to the SSO account.

    :param actor: a namedtuple with Actor details
    :param token: CSRF token required to submit the password reset form
    :param referer: (optional) referer URL
    :param next_param: (optional) URL to go to after successful password reset
    :return: response object
    """
    session = actor.session
    fab_landing = get_absolute_url("ui-buyer:landing")

    data = {
        "next": next_param or fab_landing,
        "csrfmiddlewaretoken": token,
        "email": actor.email
    }
    # Referer is the same as the final URL from the previous request
    query = "?next={}".format(next_param or fab_landing)
    referer = referer or urljoin(URL, query)
    headers = {"Referer": referer}

    response = make_request(
        Method.POST, URL, session=session, data=data, headers=headers)

    return response


def open_link(session: Session, link: str) -> Response:
    with assertion_msg("Expected a non-empty password reset email link"):
        assert link
    return make_request(Method.GET, link, session=session)
