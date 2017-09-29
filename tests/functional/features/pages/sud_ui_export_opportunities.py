# -*- coding: utf-8 -*-
"""SSO - SUD (Profile) Export Opportunities page"""
import logging

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.features.utils import Method, check_response, make_request

URL = get_absolute_url("profile:exops-applications")
EXPECTED_STRINGS = [
    "Profile", "You are signed in as", "Export opportunities", "Find a buyer",
    "Selling online overseas", "About", "Applications", "Email alerts"
]


def go_to(session: Session) -> Response:
    response = make_request(Method.GET, URL, session=session)
    return response


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug(
        "Successfully got to the SUD (Profile) Export Opportunities page")
