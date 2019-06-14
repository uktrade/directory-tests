# -*- coding: utf-8 -*-
"""FAB - Build and improve your profile - verification letter page"""
import logging

from requests import Response, Session

from tests import URLs
from tests.functional.pages import Services
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Services.FAB
NAME = "Verification letter sent"
TYPE = "confirmation"
URL = URLs.FAB_COMPANY_EDIT.absolute
EXPECTED_STRINGS = [
    "We've sent your verification letter",
    (
        "You should receive your verification letter within a week. When you"
        " receive the letter, please log in to GREAT.gov.uk to enter your "
        "verification profile to publish your company profile."
    ),
    "View or amend your company profile",
]


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on the FAB Build your profile - Confirm page")


def go_to_profile(session: Session) -> Response:
    """Supplier clicks on the 'View or amend your company profile' link."""
    url = URLs.FAB_COMPANY_PROFILE.absolute
    headers = {"Referer": URL}
    response = make_request(Method.GET, url, session=session, headers=headers)
    return response
