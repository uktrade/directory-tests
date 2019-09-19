# -*- coding: utf-8 -*-
"""FAB - Add Collaborator page"""
from requests import Response, Session

from directory_tests_shared import URLs
from tests.functional.pages import Services
from tests.functional.utils.generic import Method, make_request
from tests.functional.utils.request import check_response

SERVICE = Services.FAB
NAME = "Add collaborator"
TYPE = "form"
URL = URLs.PROFILE_ACCOUNT_ADD_COLLABORATOR.absolute
EXPECTED_STRINGS = [
    "Invite collaborators and select the role",
    "Email address of collaborator",
    "Send invite",
    "Select role",
]

EXPECTED_STRINGS_INVITATION_SENT = [
    "Collaborators invited",
    "User accounts linked to the business profile",
]


def should_be_here(response: Response, *, invitation_sent: bool = False):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)

    expected_strings = None
    if invitation_sent:
        expected_strings = EXPECTED_STRINGS_INVITATION_SENT

    if expected_strings:
        check_response(response, 200, body_contains=expected_strings)


def go_to(session: Session) -> Response:
    """Go to "Edit Company's Details" page.

    This requires:
     * Supplier to be logged in
    """
    headers = {"Referer": URLs.PROFILE_FAB.absolute}
    return make_request(Method.GET, URL, session=session, headers=headers)


def add_collaborator(session: Session, email: str) -> Response:
    data = {"email_address": email}
    headers = {"Referer": URL}
    return make_request(
        Method.POST, URL, session=session, data=data, headers=headers
    )
