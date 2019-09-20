# -*- coding: utf-8 -*-
"""International Site - Landing page"""
import logging

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Service.INTERNATIONAL
NAME = "Landing"
TYPE = PageType.LANDING
URL = URLs.INTERNATIONAL_LANDING.absolute
EXPECTED_STRINGS = ["We are Open", "The UK welcomes international business"]


def go_to(session: Session) -> Response:
    return make_request(Method.GET, URL, session=session)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the International - Landing page")
