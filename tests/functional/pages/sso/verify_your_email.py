# -*- coding: utf-8 -*-
"""SSO - Verify your email page"""
import logging

from requests import Response

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.request import check_response

SERVICE = Service.SSO
NAME = "Verify your email"
TYPE = PageType.FORM
URL = URLs.SSO_EMAIL_CONFIRM.absolute
EXPECTED_STRINGS = [
    "We'll email you a confirmation code while creating your account",
    "Make sure you have access to your email",
    "Select your business type",
]


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the SSO Verify your email page")
