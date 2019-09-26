# -*- coding: utf-8 -*-
"""ISD - Find a UK Supplier page"""
import logging

from requests import Response, Session
from retrying import retry

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.generic import (
    assertion_msg,
    escape_html,
    extract_page_contents,
)
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Service.ISD
NAME = "Search"
TYPE = PageType.SEARCH_RESULTS
URL = URLs.ISD_SEARCH.absolute
EXPECTED_STRINGS = [
    "Search results",
    "Filter results",
    "Filter by expertise",
    "New search",
]

NO_UK_BUSINESS_MATCH = "No UK businesses match your search"
NO_MATCH = [NO_UK_BUSINESS_MATCH, "Try different filters or a new search term"]


@retry(wait_fixed=5000, stop_max_attempt_number=2)
def go_to(
    session: Session, *, term: str = None, page: int = None, **kwargs
) -> Response:
    """Go to "FAS Find a Supplier" page.

    :param session: Actor's request Session
    :param term: (optional) search term
    :param page: (optional) number of search result page
    :param kwargs: (optional) search filters

    """
    allowed_search_filters = [
        "expertise_regions",
        "expertise_industries",
        "expertise_languages",
        "expertise_countries",
        "expertise_products_services_financial",
        "expertise_products_services_management",
        "expertise_products_services_human_resources",
        "expertise_products_services_legal",
        "expertise_products_services_publicity",
        "expertise_products_services_business_support",
    ]
    params = {}
    if term is not None:
        params.update({"q": term})
    if page is not None:
        params.update({"page": page})

    filter_diff = set(kwargs.keys()) - set(allowed_search_filters)
    with assertion_msg(f"Got unexpected search filters: {filter_diff}"):
        assert not filter_diff
    headers = {"Referer": URLs.PROFILE_BUSINESS_PROFILE.absolute}
    return make_request(
        Method.GET, URL, session=session, params=params, headers=headers
    )


def should_be_here(response, *, number=None):
    expected = EXPECTED_STRINGS + [number] if number else EXPECTED_STRINGS
    check_response(response, 200, body_contains=expected)
    logging.debug("Buyer is on the ISD Find a UK Supplier page")


def should_see_company(response: Response, company_title: str) -> bool:
    content = extract_page_contents(response.content.decode("utf-8")).lower()
    no_match = NO_UK_BUSINESS_MATCH.lower() in content
    contains_company_title = company_title.lower() in content
    if not contains_company_title:
        contains_company_title = escape_html(company_title).lower() in content
    if not contains_company_title:
        logging.debug(f"Could not find company: '{escape_html(company_title).lower()}'")
    return contains_company_title and not no_match


def should_not_see_company(response: Response, company_title: str) -> bool:
    content = extract_page_contents(response.content.decode("utf-8")).lower()
    return escape_html(company_title).lower() not in content


def should_see_no_matches(response: Response, *, term: str = None):
    expected = NO_MATCH
    if term:
        expected += term
    check_response(response, 200, body_contains=expected)
