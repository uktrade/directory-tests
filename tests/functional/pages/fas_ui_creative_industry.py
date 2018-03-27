# -*- coding: utf-8 -*-
"""FAS - Creative Industry page"""
import logging

from requests import Response, Session
from tests import get_absolute_url
from tests.functional.utils.request import Method, check_response, make_request

URL = get_absolute_url("ui-supplier:industries-creative")
EXPECTED_STRINGS = [
    "Delivering exceptional creative services", "Key facts",
    "Work with the best in film, TV and visual effects",
    "See the UK's creative services providers on the Find a supplier service",
    "Immersive", "Blippar", "Find other great UK companies",
    "Read more about the company", "Company showcase", "Read case study"
]


def go_to(session: Session) -> Response:
    """Go to Creative Industry Page on FAS

    :param session: Supplier session object
    :return: response object
    """
    headers = {"Referer": get_absolute_url("ui-supplier:industries")}
    return make_request(Method.GET, URL, session=session, headers=headers)


def should_be_here(response: Response):
    """Check if User is on the correct page.

    :param response: response object
    """
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on FAS Creative Industry page")
