# -*- coding: utf-8 -*-
"""FAB - Remove Collaborator page"""
from requests import Response, Session
from tests import get_absolute_url
from tests.functional.utils.generic import Method, make_request
from tests.functional.utils.request import check_response

URL = get_absolute_url("ui-buyer:account-remove-collaborator")
EXPECTED_STRINGS = [
    "Remove user from your profile",
]


def should_be_here(response: Response):
    """Check if User is on the correct page."""
    check_response(response, 200, body_contains=EXPECTED_STRINGS)


def go_to(session: Session) -> Response:
    headers = {"Referer": get_absolute_url("ui-buyer:company-profile")}
    response = make_request(Method.GET, URL, session=session, headers=headers)

    should_be_here(response)
    return response


def remove(session: Session, token: str, email: str) -> Response:
    data = {
        "csrfmiddlewaretoken": token,
        "email_address": email
    }
    headers = {"Referer": URL}
    return make_request(
        Method.POST, URL, session=session, data=data, headers=headers)


def should_not_see_collaborator(response: Response, collaborator_email: str):
    check_response(response, 200, unexpected_strings=[collaborator_email])
