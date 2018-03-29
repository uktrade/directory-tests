# -*- coding: utf-8 -*-
"""SSO - Verify your email page"""
import logging

from requests import Response
from tests.functional.utils.request import check_response

EXPECTED_STRINGS = [
    "Verify your email address",
    ("We've sent you a confirmation email. Click on the link to verify your "
     "email address."), "Contact us",
    "if you haven’t received the email within 10 minutes"
]


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the SSO Verify your email page")
