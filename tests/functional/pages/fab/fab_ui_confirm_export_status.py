# -*- coding: utf-8 -*-
"""FAB - Confirm Export Status page"""
import logging

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.pages import Services
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Services.FAB
NAME = "Confirm export status"
TYPE = "form"
URL = get_absolute_url("ui-buyer:register-confirm-export-status")
EXPECTED_STRINGS = [
    "Your company's previous exports",
    "Confirm company",
    "Trading status",
    "Have you exported before?",
    "Yes",
    "No",
    "I accept the",
    "Terms and conditions",
    "< Back to previous step",
    "Continue",
]

EXPECTED_STRINGS_WO_SSO_ACCOUNT = [
    "Creating an account means you can:",
    "promote the products or services you sell to overseas buyers",
    "give overseas buyers from your industry an easy way to find you",
    (
        "To confirm that this is your company you must create a great.gov.uk "
        "account"
    ),
]


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on Confirm Export Status page")


def submit(session: Session, token: str, exported: bool) -> Response:
    """Submit the Export Status form."""
    headers = {"Referer": URL}
    data = {
        "csrfmiddlewaretoken": token,
        "enrolment_view-current_step": "exports",
        "exports-has_exported_before": exported,
        "exports-terms_agreed": "on",
    }

    response = make_request(
        Method.POST, URL, session=session, headers=headers, data=data
    )

    return response


def should_see_info_about_sso_account(response: Response):
    """Check if Supplier is on Confirm Export Status page & info about
    SSO/great.gov.uk account is displayed.

    NOTE:
    This requires Supplier not to have a SSO account.
    """
    expected = EXPECTED_STRINGS + EXPECTED_STRINGS_WO_SSO_ACCOUNT
    check_response(response, 200, body_contains=expected)
    logging.debug("Supplier is on Confirm Export Status page")
