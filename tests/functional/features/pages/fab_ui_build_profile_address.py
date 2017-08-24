# -*- coding: utf-8 -*-
"""FAB - Build and improve your profile page"""
import logging

from requests import Response
from scrapy import Selector

from tests import get_absolute_url
from tests.functional.features.context_utils import Actor, AddressDetails
from tests.functional.features.utils import (
    Method,
    assertion_msg,
    check_response,
    make_request
)

URL = get_absolute_url("ui-buyer:company-edit")
EXPECTED_STRINGS = [
    "Your company address", "Basic", "Industry and exporting", "Confirmation",
    ("Enter your name. We’ll then send a confirmation letter to your company’s "
     "registered address address within 5 working days."),
    "Your name:", "Company number", "Tick to confirm address.",
    ("If you can’t collect the letter yourself, you’ll need to make sure "
     "someone can send it on to you."), "Back to previous step", "Send"
]


def should_be_here(response: Response):
    """Check if Supplier is on FAB Build your profile - Choose Sector page.

    :param response: response object
    """
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the FAB Build and improve your profile. "
                  "Choose Your company sector")


def extract_address_details(response: Response) -> AddressDetails:
    """Build Profile - extract address details from Your company address page.

    :param response: requests response
    :return: named tuple containing all extracted company details
    """
    with assertion_msg(
            "Could not extract Company's Address Details as the response had no"
            " content"):
        assert response.content
    content = response.content.decode("utf-8")

    def extract(selector):
        res = Selector(text=content).css(selector).extract()
        return res[0] if len(res) > 0 else ""

    address_signature = extract(
        "#ed-company-edit-address > p:nth-child(3)::attr(value)")

    details = AddressDetails(address_signature)

    logging.debug("Extracted company details: %s", details)

    return details


def submit(actor: Actor, details: AddressDetails) -> Response:
    """Build Profile - Provide Supplier's full name, which will be use when
    sending verification letter.

    :param actor: a namedtuple with Actor details
    :param details: named tuple containing extracted company address details
    :return: response object
    """
    headers = {"Referer": URL}
    data = {"csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
            "company_profile_edit_view-current_step": "address",
            "address-signature": details.address_signature,
            "address-postal_full_name": actor.alias,
            "address-address_line_1": details.address_line_1,
            "address-address_line_2": details.address_line_2,
            "address-locality": details.locality,
            "address-country": details.country,
            "address-postal_code": details.postal_code,
            "address-po_box": details.po_box
            }
    response = make_request(
        Method.POST, URL, session=actor.session, headers=headers, data=data)

    return response
