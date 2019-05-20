# -*- coding: utf-8 -*-
"""International Site - Industry page"""
import logging
from urllib.parse import urljoin

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.pages import Services
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Services.INTERNATIONAL
NAME = "Industry"
NAMES = [
    "Industry",
    "Industry (Engineering and manufacturing)",
    "Industry (Healthcare and Life Sciences)",
]
TYPE = "article"
URL = get_absolute_url("ui-international:industry")
URLs = {
    "industry": URL,
    "industry (engineering and manufacturing)": urljoin(URL, "engineering-and-manufacturing/"),
    "industry (healthcare and life sciences)": urljoin(URL, "healthcare-and-life-sciences/"),
}
EXPECTED_STRINGS = [
    "Industries",
    "Great.gov.uk International"
]


def go_to(session: Session, *, page_name: str = None) -> Response:
    url = URLs[page_name.lower()] if page_name else URL
    return make_request(Method.GET, url, session=session)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the International - Industries page")
