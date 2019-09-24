# -*- coding: utf-8 -*-
"""SSO - Registration page"""
import logging
from urllib.parse import urljoin

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.context_utils import Actor
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Service.SSO
NAME = "Register"
TYPE = PageType.FORM
URL = URLs.SSO_SIGNUP.absolute
EXPECTED_STRINGS = [
    "Register",
    "Email",
    "Confirm email",
    "Password",
    "Confirm password",
    "Your password must",
    "be at least 10 characters",
    "contain at least one letter",
    "contain at least one number",
    'not contain the word "password"',
    "Tick this box to accept the",
    "terms and conditions",
    "of the great.gov.uk service.",
]


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the SSO Registration page")


def go_to(session: Session, *, next: str = None, referer: str = None) -> Response:
    referer = referer or URLs.FAB_LANDING.absolute
    if next:
        url = urljoin(URL, f"?next={next}")
    else:
        url = URL
    headers = {"Referer": referer}
    return make_request(Method.GET, url, session=session, headers=headers)


def submit_no_company(
    actor: Actor, *, next: str = None, referer: str = URL
) -> Response:
    """Will submit the SSO Registration form without company's details.

    Used when Supplier creates a SSO/great.gov.uk account first.
    """
    session = actor.session
    headers = {"Referer": referer}
    data = {
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "email": actor.email,
        "email2": actor.email,
        "password1": actor.password,
        "password2": actor.password,
        "terms_agreed": "on",
    }
    if next:
        data["next"] = next

    return make_request(Method.POST, URL, session=session, headers=headers, data=data)
