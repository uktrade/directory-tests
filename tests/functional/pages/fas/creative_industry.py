# -*- coding: utf-8 -*-
"""Find a Supplier - Creative Industry page"""
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
NAME = "Creative services"
TYPE = PageType.INDUSTRY
URL = URLs.FAS_INDUSTRY_CREATIVE_SERVICES.absolute
EXPECTED_STRINGS = [
    "Why choose UK creative services",
    "Global appeal",
    "Talented artists",
    "State-of-the-art studios",
    "Search for UK creative companies",
]


def go_to(session: Session) -> Response:
    headers = {"Referer": URLs.FAS_INDUSTRIES.absolute}
    return make_request(Method.GET, URL, session=session, headers=headers)


def should_be_here(response: Response):
    check_url(response, URL)
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on FAS Creative Industry page")
