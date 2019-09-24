# -*- coding: utf-8 -*-
"""Find a Buyer - Change profile owner - confirm password page"""
from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.generic import Method, make_request
from tests.functional.utils.request import check_response

SERVICE = Service.FAB
NAME = "Confirm password"
TYPE = PageType.FORM
URL = URLs.FAB_ACCOUNT_CONFIRM_PASSWORD.absolute
EXPECTED_STRINGS = [
    "Transfer account",
    "Your password",
    "For your security, please enter your current password",
    "Back to previous step",
    "Confirm",
    "Cancel",
]


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)


def go_to(session: Session) -> Response:
    """Go to "Edit Company's Details" page.

    This requires:
     * Supplier to be logged in
    """
    headers = {"Referer": URL}
    return make_request(Method.GET, URL, session=session, headers=headers)


def submit(session: Session, token: str, password: str) -> Response:
    data = {
        "csrfmiddlewaretoken": token,
        "password-password": password,
        "transfer_account_wizard_view-current_step": "password",
    }
    headers = {"Referer": URL}
    return make_request(Method.POST, URL, session=session, data=data, headers=headers)
