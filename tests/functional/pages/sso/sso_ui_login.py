# -*- coding: utf-8 -*-
"""SSO - Verify your email page"""
import logging
from urllib.parse import urljoin

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.pages import Services
from tests.functional.utils.context_utils import Actor
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Services.SSO
NAME = "Login"
TYPE = "form"
URL = get_absolute_url("sso:login")
EXPECTED_STRINGS = [
    "Sign in",
    "Use your great.gov.uk login details to sign in.",
    "Email",
    "Password",
    "Forgotten password?",
    "Start now",
    "Create a great.gov.uk account",
    "It takes less than three minutes to register.",
]


def go_to(
    session: Session, *, next_param: str = None, referer: str = None
) -> Response:
    fab_landing = get_absolute_url("ui-buyer:landing")
    params = {"next": next_param or fab_landing}
    headers = {"Referer": referer or fab_landing}
    return make_request(
        Method.GET, URL, session=session, params=params, headers=headers
    )


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the SSO Verify your email page")


def login(
    actor: Actor,
    *,
    token: str = None,
    referer: str = None,
    next_param: str = None
) -> Response:
    session = actor.session
    fab_landing = get_absolute_url("ui-buyer:landing")

    data = {
        "next": next_param or fab_landing,
        "csrfmiddlewaretoken": token or actor.csrfmiddlewaretoken,
        "login": actor.email,
        "password": actor.password,
        "remember": "on",
    }
    query = f"?next={referer or fab_landing}"
    referer = urljoin(URL, query)
    headers = {"Referer": referer}

    return make_request(
        Method.POST, URL, session=session, data=data, headers=headers
    )
