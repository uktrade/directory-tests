# -*- coding: utf-8 -*-
"""Find a Buyer - Change profile owner page"""
from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.generic import Method, make_request
from tests.functional.utils.request import check_response

SERVICE = Service.FAB
NAME = "Transfer ownership"
TYPE = PageType.FORM
URL = URLs.PROFILE_ADMIN_INVITE_ADMIN.absolute
EXPECTED_STRINGS = [
    "Choose a new administrator",
    "Enter the email address of the new profile administrator",
    "Send invitation",
]


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)


def go_to(session: Session) -> Response:
    headers = {"Referer": URL}
    response = make_request(Method.GET, URL, session=session, headers=headers)

    should_be_here(response)
    return response


def submit(session: Session, email: str) -> Response:
    data = {
        "collaborator_email": email,
    }
    headers = {"Referer": URL}
    return make_request(Method.POST, URL, session=session, data=data, headers=headers)
