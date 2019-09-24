# -*- coding: utf-8 -*-
"""Find a Supplier - Landing page"""
import logging

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.generic import Method, make_request
from tests.functional.utils.request import check_response

SERVICE = Service.FAS
NAME = "Landing"
TYPE = PageType.LANDING
URL = URLs.FAS_LANDING.absolute
EXPECTED_STRINGS = [
    "Connect with UK businesses",
    "British products and services are valued worldwide for their quality",
    "Featured industries",
]


def go_to(session: Session) -> Response:
    return make_request(Method.GET, URL, session=session)


def should_be_here(response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on FAS Landing page")
