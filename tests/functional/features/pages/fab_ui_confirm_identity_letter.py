# -*- coding: utf-8 -*-
"""FAB - Confirm Identity - with letter page"""
import logging

from requests import Response

from tests import get_absolute_url
from tests.functional.features.context_utils import Actor
from tests.functional.features.utils import Method, check_response, make_request

URL = get_absolute_url("ui-buyer:confirm-identity-letter")
EXPECTED_STRINGS = [
    "Your company address", "Address",
    ("Enter your name. We’ll then send a confirmation letter to your company’s "
     "registered address address within 5 working days."),
    "Your name:", "Company number",
    "Tick to confirm address.",
    ("If you can’t collect the letter yourself, you’ll"
     " need to make sure someone can send it on to you."), "Send"
]


def should_be_here(response: Response):
    """Check if Supplier is on FAB Confirm your Identity - with letter page.

    :param response: response object
    """
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug(
        "Successfully got to the FAB Confirm your Identity - with letter page")


def submit(actor: Actor) -> Response:
    """Verify your identity with a physical letter.

    :param actor: a namedtuple with Actor details
    :return: response object
    """
    headers = {"Referer": URL}
    data = {
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "send_verification_letter_view-current_step": "address",
        "address-postal_full_name": actor.alias,
        "address-address_confirmed": "on"
    }
    response = make_request(
        Method.POST, URL, session=actor.session, headers=headers, data=data)
    return response
