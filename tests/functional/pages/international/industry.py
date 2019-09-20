# -*- coding: utf-8 -*-
"""International Site - Industry page"""
import logging
from urllib.parse import urljoin

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Service.INTERNATIONAL
NAME = "Industry"
NAMES = [
    "Creative industries",
    "Engineering and manufacturing",
    "Healthcare and Life Sciences",
    "Technology",
]
TYPE = PageType.INDUSTRY
URL = URLs.INTERNATIONAL_INDUSTRIES.absolute
SUB_URLs = {
    "creative industries": urljoin(URL, "creative-industries/"),
    "engineering and manufacturing": urljoin(URL, "engineering-and-manufacturing/"),
    "healthcare and life sciences": urljoin(URL, "healthcare-and-life-sciences/"),
    "technology": urljoin(URL, "technology/"),
}
EXPECTED_STRINGS = ["Industries", "Great.gov.uk International"]


def go_to(session: Session, *, page_name: str = None) -> Response:
    url = SUB_URLs[page_name.lower()] if page_name else URL
    return make_request(Method.GET, url, session=session)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the International - Industries page")
