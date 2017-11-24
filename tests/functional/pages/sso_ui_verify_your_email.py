# -*- coding: utf-8 -*-
"""SSO - Verify your email page"""
import logging

from requests import Response

from tests.functional.utils.request import check_response

EXPECTED_STRINGS = [
    "Verify your email address",
    ("We have sent you a confirmation email. Please follow the link in the "
     "email to verify your email address."), "Please", "contact us",
    "if you do not receive an email within 10 minutes."
]


def should_be_here(response: Response):
    """Check if Supplier is on SSO Verify your email Page.

    :param response: response object
    """
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the SSO Verify your email page")
