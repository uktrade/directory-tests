# -*- coding: utf-8 -*-
"""SSO - SUD (Profile) Find A Buyer page"""
import logging

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.features.utils import Method, check_response, make_request

URL = get_absolute_url("profile:exops-applications")
EXPECTED_STRINGS = [
    "Profile", "You are signed in as", "Export opportunities", "Find a buyer",
    "Selling online overseas", "Get a trade profile",
    "Get a trade profile for your company and you can",
    "generate new sales leads",
    "promote your business to thousands of overseas buyers",
    "add case studies of your best work to make your company stand out",
    "have buyers contact your sales team directly to get deals moving",
    "Create a trade profile"
]


def go_to(session: Session) -> Response:
    response = make_request(Method.GET, URL, session=session)
    return response


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the SUD (Profile) Find A Buyer page")
