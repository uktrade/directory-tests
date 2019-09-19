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


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)


def go_to(session: Session) -> Response:
    """Go to "Edit Company's Details" page.

    This requires:
     * Supplier to be logged in
    """
    headers = {"Referer": URLs.PROFILE_FAB.absolute}
    return make_request(Method.GET, URL, session=session, headers=headers)


def add_collaborator(session: Session, token: str, email: str) -> Response:
    data = {"csrfmiddlewaretoken": token, "email_address": email}
    headers = {"Referer": URL}
    return make_request(
        Method.POST, URL, session=session, data=data, headers=headers
    )
