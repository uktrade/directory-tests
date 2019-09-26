# -*- coding: utf-8 -*-
"""Find a Buyer - Add Collaborator page"""
from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.generic import Method, make_request
from tests.functional.utils.request import check_response

SERVICE = Service.FAB
NAME = "Add collaborator"
TYPE = PageType.FORM
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
    headers = {"Referer": URLs.PROFILE_BUSINESS_PROFILE.absolute}
    return make_request(Method.GET, URL, session=session, headers=headers)


def add_collaborator(session: Session, email: str, role: str) -> Response:
    data = {"collaborator_email": email, "role": role.upper()}
    headers = {"Referer": URL}
    return make_request(Method.POST, URL, session=session, data=data, headers=headers)
