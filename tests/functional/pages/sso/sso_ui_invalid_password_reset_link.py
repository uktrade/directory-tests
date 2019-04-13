# -*- coding: utf-8 -*-
"""SSO - Invalid password reset link page"""
import logging

from requests import Response
from tests.functional.utils.request import check_response

EXPECTED_STRINGS = [
    "Bad Token",
    "Please request a",
    "new password reset",
    (
        "The password reset link was invalid, possibly because it has already "
        "been used."
    ),
]


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Got to the SSO Invalid Password Reset Link page")
