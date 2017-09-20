# -*- coding: utf-8 -*-
"""SSO - Verify your email page"""
import logging

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.features.context_utils import Actor
from tests.functional.features.utils import Method, check_response, make_request

URL = get_absolute_url("sso:login")
EXPECTED_STRINGS = [
    "Sign in", "If you have not created an account yet, then please",
    "register", "first.", "Email:", "Password:", "Remember me:", "Login",
    "Reset your password"
]


def go_to(session: Session) -> Response:
    fab_landing = get_absolute_url("ui-buyer:landing")
    params = {"next": fab_landing}
    headers = {"Referer": fab_landing}
    response = make_request(
        Method.GET, URL, session=session, params=params, headers=headers)
    return response


def should_be_here(response: Response):
    """Check if Supplier is on SSO Verify your email Page.

    :param response: response object
    """
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the SSO Verify your email page")


def login(
        actor: Actor, token: str, *, referer: str = None,
        next: str = None) -> Response:
    """Try to sign in to FAB as a Supplier without verified email address.

    :param actor: a namedtuple with Actor details
    :param token: CSRF token required to submit the login form
    :param referer: (optional) referer URL
    :param next: (optional) URL to go to after successful login
    :return: response object
    """
    session = actor.session
    fab_landing = get_absolute_url("ui-buyer:landing")

    data = {
        "next": fab_landing,
        "csrfmiddlewaretoken": token,
        "login": actor.email,
        "password": actor.password,
        "remember": "on"
    }
    if next:
        data.update({"next": next})
    # Referer is the same as the final URL from the previous request
    referer = referer or "{}?next={}".format(URL, fab_landing)
    headers = {"Referer": referer}

    response = make_request(
        Method.POST, URL, session=session, data=data, headers=headers)

    return response
