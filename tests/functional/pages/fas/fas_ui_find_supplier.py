# -*- coding: utf-8 -*-
"""FAS - Find a Supplier page"""
import logging

from requests import Response, Session
from retrying import retry

from tests import get_absolute_url
from tests.functional.pages import Services
from tests.functional.utils.generic import escape_html, extract_page_contents
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Services.FAS
NAME = "Search"
TYPE = "search"
URL = get_absolute_url("ui-supplier:search")
EXPECTED_STRINGS = [
    "Search results",
    "Filter results",
    "New search",
]

NO_UK_BUSINESS_MATCH = "No UK businesses match your search"
NO_MATCH = [
    NO_UK_BUSINESS_MATCH,
    "Try different filters or a new search term",
]


@retry(wait_fixed=5000, stop_max_attempt_number=2)
def go_to(
    session: Session, *, term: str = None, page: int = None, sectors: list = None
) -> Response:
    """Go to "FAS Find a Supplier" page.

    :param term: (optional) search term
    :param page: (optional) number of search result page
    :param sectors: (optional) a list of Industry sector filters
    """
    params = {}
    if term is not None:
        params.update({"q": term})
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
    content = extract_page_contents(response.content.decode("utf-8")).lower()
    no_match = NO_UK_BUSINESS_MATCH.lower() in content
    contains_company_title = escape_html(company_title).lower() in content
    if not contains_company_title:
        logging.debug(
            f"Could not find company: {escape_html(company_title).lower()} in "
            f"the response:\n{content}")
    return contains_company_title and not no_match


def should_not_see_company(response: Response, company_title: str) -> bool:
    content = extract_page_contents(response.content.decode("utf-8")).lower()
    return escape_html(company_title).lower() not in content


def should_see_no_matches(response: Response, *, term: str = None):
    expected = NO_MATCH
    if term:
        expected += term
    check_response(response, 200, body_contains=expected)
