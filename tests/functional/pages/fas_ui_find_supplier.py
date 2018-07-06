# -*- coding: utf-8 -*-
"""FAS - Find a Supplier page"""
import logging

from requests import Response, Session
from tests import get_absolute_url
from tests.functional.utils.generic import escape_html
from tests.functional.utils.request import Method, check_response, make_request

URL = get_absolute_url("ui-supplier:search")
EXPECTED_STRINGS = [
    "Find UK Suppliers",
    "Search by product, service or company keyword",
    "Search",
]

NO_MATCH = [
    "Your search",
    '&quot;<span class="term">',
    "</span>&quot;",
    "did not match any UK trade profiles.",
]


def go_to(
    session: Session,
    *,
    term: str = None,
    page: int = None,
    sectors: list = None
) -> Response:
    """Go to "FAS Find a Supplier" page.

    :param term: (optional) search term
    :param page: (optional) number of search result page
    :param sectors: (optional) a list of Industry sector filters
    """
    params = {}
    if term is not None:
        params.update({"term": term})
    if page is not None:
        params.update({"page": page})
    if sectors is not None:
        params.update({"sectors": sectors})
    headers = {"Referer": get_absolute_url("ui-buyer:company-profile")}
    return make_request(
        Method.GET, URL, session=session, params=params, headers=headers
    )


def should_be_here(response, *, number=None):
    expected = EXPECTED_STRINGS + [number] if number else EXPECTED_STRINGS
    check_response(response, 200, body_contains=expected)
    logging.debug("Buyer is on the FAS Find a Supplier page")


def should_see_company(response: Response, company_title: str) -> bool:
    content = response.content.decode("utf-8").lower()
    no_match = "did not match any uk trade profiles" in content
    contains_company_title = escape_html(company_title).lower() in content
    return contains_company_title and not no_match


def should_not_see_company(response: Response, company_title: str) -> bool:
    content = response.content.decode("utf-8")
    return escape_html(company_title, upper=True) not in content


def should_see_no_matches(response: Response, *, term: str = None):
    expected = NO_MATCH
    if term:
        expected += term
    check_response(response, 200, body_contains=expected)
