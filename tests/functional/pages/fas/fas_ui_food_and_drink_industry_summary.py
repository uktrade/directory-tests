# -*- coding: utf-8 -*-
"""FAS - Food and Drink Industry page"""
import logging

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.pages import Services
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Services.FAS
NAME = "Food and drink industry"
TYPE = "summary"
URL = get_absolute_url("ui-supplier:industries-food-summary")
EXPECTED_STRINGS = [
    "UK food and drink",
    "Find your UK trade partner",
    "See the UK's food and drink companies on the Find a supplier service",
    "Joe &amp; Seph&#39;s",
    "Fever-Tree",
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
    logging.debug("Supplier is on FAS Food and Drink Industry page")