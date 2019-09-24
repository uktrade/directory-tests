# -*- coding: utf-8 -*-
"""Find a Buyer - Change profile owner page"""
from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.generic import Method, make_request
from tests.functional.utils.request import check_response

SERVICE = Service.FAB
NAME = "Transfer ownership"
TYPE = PageType.FORM
URL = URLs.FAB_ACCOUNT_TRANSFER_OWNERSHIP.absolute
EXPECTED_STRINGS = [
    "Transfer account",
    "Next",
    "Cancel",
    "Enter the email address of the new administrator",
]


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)


def go_to(session: Session) -> Response:
    """Go to "Edit Company's Details" page.

    This requires:
     * Supplier to be logged in
    """
    headers = {"Referer": URLs.PROFILE_FAB.absolute}
    response = make_request(Method.GET, URL, session=session, headers=headers)

    should_be_here(response)
    return response


def submit(session: Session, token: str, email: str) -> Response:
    data = {
        "csrfmiddlewaretoken": token,
        "email-email_address": email,
        "transfer_account_wizard_view-current_step": "email",
    }
    headers = {"Referer": URL}
    return make_request(Method.POST, URL, session=session, data=data, headers=headers)
