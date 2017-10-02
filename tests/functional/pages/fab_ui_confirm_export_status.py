# -*- coding: utf-8 -*-
"""FAB - Confirm Export Status page"""
import logging

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.utils.request import Method, check_response, make_request

EXPECTED_STRINGS = [
    "Your company's previous exports", "Confirm company", "Export status",
    "Have you exported before?",
    "Yes", "No", "I accept the", "Find a Buyer terms and conditions",
    "< Back to previous step", "Continue"
]

EXPECTED_STRINGS_WO_SSO_ACCOUNT = [
    "An account will let you:",
    "Create a trade profile that will be promoted to international businesses",
    "Apply for export opportunities sourced by UK embassies worldwide",
    ("To confirm that this is your company you must create a great.gov.uk "
     "account")
]


def should_be_here(response: Response):
    """Check if Supplier is on Confirm Export Status page.

    :param response: response with Confirm Export Status page
    """
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on Confirm Export Status page")


def submit(session: Session, token: str, exported: bool) -> Response:
    """Submit the Export Status form.

    :param session: Supplier session object
    :param token: a CSRF token required to submit the form
    :param exported: True is exported in the past, False if not
    :return: response object
    """
    url = get_absolute_url("ui-buyer:register-confirm-export-status")
    headers = {"Referer": url}
    data = {
        "csrfmiddlewaretoken": token,
        "enrolment_view-current_step": "exports",
        "exports-has_exported_before": exported,
        "exports-terms_agreed": "on"
    }

    response = make_request(
        Method.POST, url, session=session, headers=headers, data=data)

    return response


def should_see_info_about_sso_account(response: Response):
    """Check if Supplier is on Confirm Export Status page & info about
    SSO/great.gov.uk account is displayed.

    NOTE:
    This requires Supplier not to have a SSO account.

    :param response: response with Confirm Export Status page
    """
    expected = EXPECTED_STRINGS + EXPECTED_STRINGS_WO_SSO_ACCOUNT
    check_response(response, 200, body_contains=expected)
    logging.debug("Supplier is on Confirm Export Status page")
