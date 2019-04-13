# -*- coding: utf-8 -*-
"""FAS - Landing page"""
import logging

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.pages import Services
from tests.functional.utils.generic import Method, make_request
from tests.functional.utils.request import check_response

SERVICE = Services.FAS
NAME = "Landing"
TYPE = "landing"
URL = get_absolute_url("ui-supplier:landing")
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
