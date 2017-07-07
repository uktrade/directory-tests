# -*- coding: utf-8 -*-
"""FAB - Edit Company's Directory Profile page"""
import logging

from faker import Factory

from tests import get_absolute_url
from tests.functional.features.pages import fab_ui_profile
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


def should_be_here(response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on the Company's Address page")


def update_letters_recipient(
        context, supplier_alias, *, update=True, full_name=None):
    """Update the full name of the letters recipient.

    If `update` is False then the current letter recipient will be used.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :param update: update recipient if True, or use the current one if False
    :param full_name: use specific full name of letter recipient if provided
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session
    token = actor.csrfmiddlewaretoken
    company = context.get_company(actor.company_alias)
    address = company.address_details

    if update:
        new_full_name = full_name or FAKE.name()
    else:
        new_full_name = address.letter_recipient

    headers = {"Referer": URL}
    data = {"csrfmiddlewaretoken": token,
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

    response = make_request(Method.POST, URL, session=session, headers=headers,
                            data=data, allow_redirects=True, context=context)

    fab_ui_profile.should_be_here(response)
    context.set_company_details(company.alias, letter_recipient=new_full_name)
    logging.debug("%s set letter recipient full name to: %s",
                  supplier_alias, new_full_name)
