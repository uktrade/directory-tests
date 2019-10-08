# -*- coding: utf-8 -*-
"""Domestic Site - Home page"""
import logging

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Service.DOMESTIC
NAME = "Home"
TYPE = PageType.HOME
URL = URLs.DOMESTIC_LANDING.absolute
EXPECTED_STRINGS = [
    "IF WE CAN",
    "YOU CAN",
    "Thousands of businesses like yours have increased their sales",
]


def go_to(session: Session) -> Response:
    return make_request(Method.GET, URL, session=session)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the Domestic - Home page")
