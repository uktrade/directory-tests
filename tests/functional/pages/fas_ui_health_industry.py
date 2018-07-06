# -*- coding: utf-8 -*-
"""FAS - Health Industry page"""
import logging

from requests import Response, Session
from tests import get_absolute_url
from tests.functional.utils.request import Method, check_response, make_request

URL = get_absolute_url("ui-supplier:industries-health")
EXPECTED_STRINGS = [
    "Delivering the exceptional in healthcare and life sciences",
    "Key facts",
    "Work with the UK to create first-rate healthcare",
    (
        "See the UK's healthcare and life sciences providers on the Find a "
        "supplier service"
    ),
    "RD Biomed",
    "Touch Bionics",
    "Find other great UK companies",
    "Read more about the company",
    "Company showcase",
    "Read case study",
]


def go_to(session: Session) -> Response:
    headers = {"Referer": get_absolute_url("ui-supplier:industries")}
    return make_request(Method.GET, URL, session=session, headers=headers)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on FAS Health Industry page")
