# -*- coding: utf-8 -*-
"""Find a Supplier - Health Industry page"""
import logging

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.request import (
    Method,
    check_response,
    check_url,
    make_request,
)

SERVICE = Service.FAS
NAME = "Health"
TYPE = PageType.INDUSTRY
URL = URLs.FAS_INDUSTRY_HEALTHCARE.absolute
EXPECTED_STRINGS = [
    "Why choose UK healthcare",
    "World-class infrastructure",
    "Innovative healthcare",
    "Pioneering technology",
]


def go_to(session: Session) -> Response:
    headers = {"Referer": URLs.FAS_INDUSTRIES.absolute}
    return make_request(Method.GET, URL, session=session, headers=headers)


def should_be_here(response: Response):
    check_url(response, URL)
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on FAS Health Industry page")
