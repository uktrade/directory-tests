# -*- coding: utf-8 -*-
"""FAB - Edit the name of the letters recipient"""
import logging

from faker import Factory
from requests import Response

from tests import get_absolute_url
from tests.functional.features.context_utils import Actor, Company
from tests.functional.features.utils import Method, check_response, make_request

URL = get_absolute_url("ui-buyer:company-edit")
EXPECTED_STRINGS = [
    "Your company address",
    ("We need to send a letter containing a verification code to your business "
     "address. This is an additional step to validate that you do represent "
     "your business."),
    "Full name:", "This is the full name that letters will be addressed to.",
    "Address line 1:", "Address line 2:", "City:", "Country:", "Postcode:",
    "PO box:", "Back to previous step", "Save"
]
FAKE = Factory.create()


def should_be_here(response: Response):
    """Check if Supplier is on the 'Edit the name of letters recipient' page.

    :param response: a response object
    """
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on the Company's Address page")


def update_letters_recipient(
        actor: Actor, company: Company, *, update: bool = True,
        full_name: bool = None) -> Response:
    """Update the full name of the letters recipient.

    If `update` is False then the current letter recipient will be used.

    :param actor: a namedtuple with Actor details
    :param company: a namedtuple with Company details
    :param update: update recipient if True, or use the current one if False
    :param full_name: use specific full name of letter recipient if provided
    :return: a response object.
    """
    session = actor.session
    token = actor.csrfmiddlewaretoken
    address = company.address_details

    if update:
        new_full_name = full_name or FAKE.name()
    else:
        new_full_name = address.letter_recipient

    headers = {"Referer": URL}
    data = {
        "csrfmiddlewaretoken": token,
        "supplier_company_profile_edit_view-current_step": "address",
        "address-signature": address.address_signature,
        "address-postal_full_name": new_full_name,
        "address-address_line_1": address.address_line_1,
        "address-address_line_2": address.address_line_2,
        "address-locality": address.locality,
        "address-country": address.country,
        "address-postal_code": address.postal_code,
        "address-po_box": address.po_box
    }

    return make_request(
        Method.POST, URL, session=session, headers=headers, data=data)
