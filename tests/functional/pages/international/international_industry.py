# -*- coding: utf-8 -*-
"""International Site - Industry page"""
import logging

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.pages import Services
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Services.INTERNATIONAL
NAME = "Industry"
TYPE = "article"
URL = get_absolute_url("ui-international:industry")
EXPECTED_STRINGS = [
    "Industries",
    "Great.gov.uk International"
]


def go_to(session: Session) -> Response:
    return make_request(Method.GET, URL, session=session)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the International - Industries page")
