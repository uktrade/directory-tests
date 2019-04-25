# -*- coding: utf-8 -*-
"""FAS - Creative Industry page"""
import logging

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.pages import Services
from tests.functional.utils.request import (
    Method,
    check_response,
    check_url,
    make_request,
)

SERVICE = Services.FAS
NAME = "Creative"
TYPE = "industry"
URL = get_absolute_url("ui-supplier:industries-creative")
EXPECTED_STRINGS = [
    "Why choose UK creative services",
    "Global appeal",
    "Talented artists",
    "State-of-the-art studios",
    "Search for UK creative companies",
]


def go_to(session: Session) -> Response:
    headers = {"Referer": get_absolute_url("ui-supplier:industries")}
    return make_request(Method.GET, URL, session=session, headers=headers)


def should_be_here(response: Response):
    check_url(response, URL)
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on FAS Creative Industry page")
