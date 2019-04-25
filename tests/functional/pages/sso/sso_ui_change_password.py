# -*- coding: utf-8 -*-
"""SSO - Change password page"""
import logging
from urllib.parse import urljoin

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.pages import Services
from tests.functional.utils.context_utils import Actor
from tests.functional.utils.generic import assertion_msg
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Services.SSO
NAME = "Change password"
TYPE = "form"
URL = get_absolute_url("sso:password_change")
EXPECTED_STRINGS = ["Change Password", "New password", "Confirm password"]


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the SSO Change Password page")


def submit(
    actor: Actor,
    action: str,
    *,
    password: str = None,
    password_again: str = None,
    referer: str = None
) -> Response:
    session = actor.session
    URL = urljoin(get_absolute_url("sso:landing"), action)
    profile_about = get_absolute_url("profile:about")

    data = {
        "action": "change password",
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "password1": password or actor.password,
        "password2": password_again or password or actor.password,
    }
    # Referer is the same as the final URL from the previous request
    query = f"?next={referer or profile_about}"
    referer = urljoin(URL, query)
    headers = {"Referer": referer}

    response = make_request(
        Method.POST, URL, session=session, data=data, headers=headers
    )

    return response


def open_password_reset_link(session: Session, link: str) -> Response:
    with assertion_msg("Expected a non-empty password reset email link"):
        assert link
    return make_request(Method.GET, link, session=session)
