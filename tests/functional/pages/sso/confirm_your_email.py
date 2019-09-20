# -*- coding: utf-8 -*-
"""SSO - Verify your email page"""
import logging
from urllib.parse import unquote, urljoin

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.context_utils import Actor
from tests.functional.utils.generic import assertion_msg
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Service.SSO
NAME = "Confirm your email"
TYPE = PageType.FORM
URL = URLs.SSO_EMAIL_CONFIRM.absolute
EXPECTED_STRINGS = [
    "Confirm email address",
    "Confirm that ",
    "is an email address for user",
]


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the SSO Confirm your email page")


def open_confirmation_link(session: Session, link: str) -> Response:
    with assertion_msg("Expected a non-empty email confirmation link"):
        assert link
    return make_request(Method.GET, link, session=session)


def confirm(actor: Actor, form_action_value: str) -> Response:
    """Confirm the email address provided by the Supplier.

    :param form_action_value: form action from SSO Confirm your email page
    """
    session = actor.session
    # in order to be redirected to the correct URL we have `unquote`
    # the form_action_value
    url = urljoin(URLs.SSO_LANDING.absolute, unquote(form_action_value))
    headers = {"Referer": url}
    data = {"csrfmiddlewaretoken": actor.csrfmiddlewaretoken}

    return make_request(Method.POST, url, session=session, headers=headers, data=data)
