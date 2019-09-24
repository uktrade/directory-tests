# -*- coding: utf-8 -*-
"""Find a Buyer - Confirm your want to become the new owner of company's profile page"""
import logging

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.generic import assertion_msg
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Service.FAB
NAME = "Confirm company ownership"
TYPE = PageType.FORM
URL = URLs.FAB_ACCOUNT_CONFIRM_OWNERSHIP_TRANSFER.absolute
EXPECTED_STRINGS = [
    "Transfer account",
    "Do you accept transfer of the company profile for",
    "Yes",
    "No",
]


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the FAB Confirm your ownership page")


def open(session: Session, link: str) -> Response:
    with assertion_msg("Expected a non-empty account transfer request link"):
        assert link
    return make_request(Method.GET, link, session=session)


def confirm(session: Session, csrf_middleware_token: str, link: str) -> Response:
    # in order to be redirected to the correct URL we have `unquote`
    # the form_action_value
    start = link.index("=") + 1
    invite_key = link[start:]
    headers = {"Referer": link}
    data = {"csrfmiddlewaretoken": csrf_middleware_token, "invite_key": invite_key}

    return make_request(Method.POST, link, session=session, headers=headers, data=data)
