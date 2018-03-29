# -*- coding: utf-8 -*-
"""FAB - Build and improve your profile page"""
import logging

from requests import Response
from tests import get_absolute_url
from tests.functional.utils.context_utils import Actor
from tests.functional.utils.request import Method, check_response, make_request

URL = get_absolute_url("ui-buyer:company-edit")
EXPECTED_STRINGS = [
    "Your company address", "About your company", "Industry and exporting",
    "Confirmation",
    ("Enter your name. We’ll then send a confirmation letter to your company’s"
     " registered address address within 5 working days."),
    "Your name:", "Company number", "Tick to confirm address.",
    ("If you can’t collect the letter yourself, you’ll need to make sure "
     "someone can send it on to you."), "Back to previous step", "Send"
]


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug(
        "Successfully got to the FAB Build and improve your profile. Choose "
        "Your company sector")


def submit(actor: Actor) -> Response:
    """Build Profile - Provide Supplier's full name, which will be use when
    sending verification letter.
    """
    headers = {"Referer": URL}
    data = {
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "company_profile_edit_view-current_step": "address",
        "address-postal_full_name": actor.alias,
        "address-address_confirmed": "on"
    }
    return make_request(
        Method.POST, URL, session=actor.session, headers=headers, data=data)
