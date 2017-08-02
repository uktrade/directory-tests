# -*- coding: utf-8 -*-
"""SSO - Verify your email page"""
import logging
from urllib.parse import unquote

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.features.context_utils import Actor
from tests.functional.features.utils import (
    Method,
    assertion_msg,
    check_response,
    make_request
)

EXPECTED_STRINGS = [
    "Confirm email Address", "Please confirm that", "is an email",
    "address for user"
]


def should_be_here(response: Response):
    """Check if Supplier is on SSO Confirm your email Page.

    :param response: response object
    """
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the SSO Confirm your email page")


def open_confirmation_link(session: Session, link: str) -> Response:
    """Open email confirmation link sent to the Supplier.

    :param session: Supplier session object
    :param link: email confirmation link
    :return: response object
    """
    with assertion_msg("Expected a non-empty email confirmation link"):
        assert link
    response = make_request(Method.GET, link, session=session)
    return response


def confirm(actor: Actor, form_action_value: str) -> Response:
    """Confirm the email address provided by the Supplier.

    :param actor: a namedtuple with Actor details
    :param form_action_value: form action from SSO Confirm your email page
    :return: response object
    """
    session = actor.session
    # in order to be redirected to the correct URL we have `unquote`
    # the form_action_value
    url = "{}{}".format(
        get_absolute_url("sso:landing"), unquote(form_action_value))
    headers = {"Referer": url}
    data = {"csrfmiddlewaretoken": actor.csrfmiddlewaretoken}

    return make_request(
        Method.POST, url, session=session, headers=headers, data=data)
