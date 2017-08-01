# -*- coding: utf-8 -*-
"""FAS - Find a Supplier page"""
import logging

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.features.utils import Method, check_response, make_request

URL = get_absolute_url("ui-supplier:search")
EXPECTED_STRINGS = [
    "Find UK Suppliers",
    "Search by product, service or company keyword",
    "Search"
]


def go_to(session: Session, *, term: str = None) -> Response:
    """Go to "FAS Find a Supplier" page.

    :param session: Supplier session object
    :param term: (optional) search term
    :return: response object
    """
    params = {"term": term} if term else {}
    headers = {"Referer": get_absolute_url("ui-buyer:company-profile")}
    response = make_request(
        Method.GET, URL, session=session, params=params, headers=headers)

    should_be_here(response)
    if term:
        logging.debug("Buyer searched for Suppliers using term: %s", term)
    else:
        logging.debug("Buyer is on the FAS Find a Supplier page")
    return response


def should_be_here(response, *, number=None):
    expected = EXPECTED_STRINGS + [number] if number else EXPECTED_STRINGS
    check_response(response, 200, body_contains=expected)
    logging.debug("Buyer is on FAS Company's Profile page")


def should_see_company(response: Response, company_title: str) -> bool:
    content = response.content.decode("utf-8")
    return company_title in content


def should_not_see_company(response: Response, company_title: str) -> bool:
    content = response.content.decode("utf-8")
    return company_title not in content
