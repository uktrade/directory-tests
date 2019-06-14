# -*- coding: utf-8 -*-
"""FAB - Confirm Identity - with letter page"""
import logging

from requests import Response, Session

from tests import URLs
from tests.functional.pages import Services
from tests.functional.utils.context_utils import Actor
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Services.FAB
NAME = "Confirm identity with letter"
TYPE = "form"
URL = URLs.FAB_CONFIRM_IDENTITY_LETTER.absolute
EXPECTED_STRINGS = [
    "Verification letter request",
    "Your verification letter should arrive within 5 working days",
    "The letter contains a 12 digit verification code"
]


def go_to(session: Session) -> Response:
    headers = {"Referer": URL}
    return make_request(Method.GET, URL, session=session, headers=headers)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug(
        "Successfully got to the FAB Confirm your Identity - with letter page"
    )


def submit(actor: Actor) -> Response:
    """Verify your identity with a physical letter."""
    headers = {"Referer": URL}
    data = {
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "send_verification_letter_view-current_step": "address",
        "address-postal_full_name": actor.alias,
        "address-address_confirmed": "on",
    }
    response = make_request(
        Method.POST, URL, session=actor.session, headers=headers, data=data
    )
    return response
