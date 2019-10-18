# -*- coding: utf-8 -*-
"""Find a Supplier - Find a Supplier page"""
import logging
from typing import List

from requests import Response, Session
from retrying import retry
from scrapy import Selector

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.generic import escape_html, extract_page_contents
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Service.FAS
NAME = "Search"
TYPE = PageType.SEARCH
URL = URLs.FAS_SEARCH.absolute
EXPECTED_STRINGS = ["Search results", "Filter results", "New search"]

NO_UK_BUSINESS_MATCH = "No UK businesses match your search"
NO_MATCH = [NO_UK_BUSINESS_MATCH, "Try different filters or a new search term"]
ENTER_SEARCH_TERM_OR_USE_FILTERS = ["Enter a search term or use the filters"]


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
        # remove words which make FAS return hundreds of result pages
        term = term.replace("LTD", "").replace("LIMITED", "")
        params.update({"q": term})
    if page is not None:
        params.update({"page": page})
    if sectors is not None:
        params.update({"sectors": sectors})
    headers = {"Referer": URLs.PROFILE_BUSINESS_PROFILE.absolute}
    return make_request(
        Method.GET, URL, session=session, params=params, headers=headers, trim=False
    )


def should_be_here(response, *, number=None):
    expected = EXPECTED_STRINGS + [number] if number else EXPECTED_STRINGS
    check_response(response, 200, body_contains=expected)
    logging.debug("Buyer is on the FAS Find a Supplier page")


def get_profile_links(page_content: str) -> List[tuple]:
    profile_selector = "#companies-column > ul > li a"
    profile_links = Selector(text=page_content).css(profile_selector).extract()
    results = []
    for link in profile_links:
        href = Selector(text=link).css("a::attr(href)").extract()[0]
        company_title = Selector(text=link).css("h3::text").extract()[0]
        clean_company_title = escape_html(company_title.replace("  ", " ")).lower()
        results.append((clean_company_title, href))
    return results


def find_profile_link(response: Response, company_title: str) -> str:
    raw_content = response.content.decode("utf-8")
    content = extract_page_contents(raw_content).lower()

    no_match = NO_UK_BUSINESS_MATCH.lower() in content
    if no_match:
        logging.warning(NO_UK_BUSINESS_MATCH)
        return ""

    profile_links = get_profile_links(raw_content)
    logging.debug(f"List of found profiles: {profile_links}")

    clean_company_title = escape_html(company_title.replace("  ", " ")).lower()
    for title, href in profile_links:
        if title == clean_company_title:
            logging.debug(f"Found link to '{clean_company_title}' profile: {href}")
            return href
    return ""


def should_not_see_company(response: Response, company_title: str) -> bool:
    content = extract_page_contents(response.content.decode("utf-8")).lower()
    return escape_html(company_title).lower() not in content


def should_see_no_matches(response: Response, *, term: str = None):
    expected = NO_MATCH
    if term:
        expected += term
    check_response(response, 200, body_contains=expected)


def should_see_no_results(response: Response, *, term: str = None):
    expected = ENTER_SEARCH_TERM_OR_USE_FILTERS
    if term:
        expected += term
    check_response(response, 200, body_contains=expected)
