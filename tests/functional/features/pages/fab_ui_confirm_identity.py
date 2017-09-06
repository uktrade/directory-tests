# -*- coding: utf-8 -*-
"""FAB - Confirm Identity page"""
import logging

from requests import Response

from tests import get_absolute_url
from tests.functional.features.context_utils import Actor
from tests.functional.features.utils import Method, check_response, make_request

URL = get_absolute_url("ui-buyer:confirm-identity")
EXPECTED_STRINGS = [
    "Confirm your identity",
    "For security, we need to check you’re who you say you are.",
    ("You can sign in with Companies House to confirm your identity straight "
     "away. You’ll need your Companies House username and password."),
    ("Alternatively, we can send a confirmation letter to your company’s "
     "registered address."),
    "Sign in with Companies House",
    ("Enter your Companies House username and password. We’ll be able to "
     "confirm your identity instantly."),
    "Sign in", "Get confirmation letter",
    ("We’ll then send a confirmation letter to your company’s registered "
     "address address within 5 working days. If you can’t collect the letter "
     "yourself, you’ll need to make sure someone can send it on to you."),
    "Send", "Back"
]


def should_be_here(response: Response):
    """Check if Supplier is on FAB Confirm your Identity page.

    :param response: response object
    """
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the FAB Confirm your Identity page")


def send(actor: Actor) -> Response:
    """Choose to verify your identity with a physical letter.

    :param actor: a namedtuple with Actor details
    :return: response object
    """
    headers = {"Referer": URL}
    letter_url = get_absolute_url("ui-buyer:confirm-identity-letter")
    response = make_request(
        Method.GET, letter_url, session=actor.session, headers=headers)
    return response
