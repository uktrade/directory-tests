# -*- coding: utf-8 -*-
"""FAB - Change profile owner page"""
from requests import Response, Session
from tests import get_absolute_url
from tests.functional.utils.generic import Method, make_request
from tests.functional.utils.request import check_response

URL = get_absolute_url("ui-buyer:account-transfer-ownership")
EXPECTED_STRINGS = [
    "Transfer account", "Next", "Cancel",
    "Enter the email address you want your profile transferred to."
]


def should_be_here(response: Response):
    """Check if User is on the correct page."""
    check_response(response, 200, body_contains=EXPECTED_STRINGS)


def go_to(session: Session) -> Response:
    """Go to "Edit Company's Details" page.

    This requires:
     * Supplier to be logged in

    """
    headers = {"Referer": get_absolute_url("profile:fab")}
    response = make_request(Method.GET, URL, session=session, headers=headers)

    should_be_here(response)
    return response


def submit(session: Session, token: str, email: str) -> Response:
    data = {
        "csrfmiddlewaretoken": token,
        "email-email_address": email,
        "transfer_account_wizard_view-current_step": "email"
    }
    headers = {"Referer": URL}
    return make_request(
        Method.POST, URL, session=session, data=data, headers=headers)
