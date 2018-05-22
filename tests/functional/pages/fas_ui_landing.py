# -*- coding: utf-8 -*-
"""FAS - Landing page"""
import logging

from requests import Response, Session
from scrapy import Selector
from tests import get_absolute_url
from tests.functional.utils.request import Method, check_response, make_request

URL = get_absolute_url("ui-supplier:landing")
PAGE_TITLE = \
    "Find trade profiles of reliable UK suppliers - trade.great.gov.uk"
EXPECTED_STRINGS = [
    PAGE_TITLE
]

SECTIONS = {
    "hero": {
        "itself": "section#hero",
    },
    "find uk suppliers": {
        "itself": "#search-area",
        "search term input": "#id_term",
        "search selectors dropdown": "#id_sectors",
        "find suppliers button": "#search-area > form button"
    },
    "contact us": {
        "itself": "#introduction-section",
        "introduction text": "#introduction-section p",
        "contact us button": "#introduction-section a"
    },
    "uk industries": {
        "itself": "#industries-section",
        "first industry": "#industries-section a:nth-child(1)",
        "second industry": "#industries-section a:nth-child(2)",
        "third industry": "#industries-section a:nth-child(3)",
        "see more button": "#industries-section > div > a.button"
    },
    "uk services": {
        "itself": "#services-section",
        "first service": "#services-section div.column-one-quarter:nth-child(3)",
        "second service": "#services-section div.column-one-quarter:nth-child(4)",
        "third service": "#services-section div.column-one-quarter:nth-child(5)",
        "fourth service": "#services-section div.column-one-quarter:nth-child(6)",
    }
}


def check_for_section(
        content: str, all_sections: dict, sought_section: str):
    """Check if all page elements from sought section are visible."""
    section = all_sections[sought_section.lower()]
    for element_name, selector in section.items():
        element = Selector(text=content).css(selector)
        assert element is not None


def go_to(session: Session) -> Response:
    response = make_request(Method.GET, URL, session=session)
    should_be_here(response)
    return response


def should_be_here(response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Buyer is on FAS Landing (home) page")


def should_see_section(content: str, name: str):
    check_for_section(content, SECTIONS, sought_section=name)
