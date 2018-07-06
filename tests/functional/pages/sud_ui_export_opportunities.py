# -*- coding: utf-8 -*-
"""SSO - SUD (Profile) Export Opportunities page"""
import logging

from requests import Response, Session
from tests import get_absolute_url
from tests.functional.utils.request import Method, check_response, make_request

URL = get_absolute_url("profile:exops-applications")
EXPECTED_STRINGS = [
    "Profile", "You are signed in as", "Export opportunities", "Find a buyer",
    "Selling online overseas",
    "Start applying for export opportunities. You can quickly and easily:",
    "find thousands of exporting opportunities",
    "search for opportunities within your industry or in a specific country",
    ("sign up for email alerts so you're the first to know of new "
     "opportunities"),
    "apply for any export opportunity and track your applications",
    "Find and apply"
]


def go_to(session: Session) -> Response:
    return make_request(Method.GET, URL, session=session)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug(
        "Successfully got to the SUD (Profile) Export Opportunities page")
