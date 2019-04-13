# -*- coding: utf-8 -*-
"""FAS - Industries page"""
import logging

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.pages import Services
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Services.FAS
NAME = "Industries"
TYPE = "listing"
URL = get_absolute_url("ui-supplier:industries")
EXPECTED_STRINGS = [
    "Discover the UK's capability in these key industries",
    "UK industries",
]
EXPECTED_STRINGS_HEALTH = [
    "Healthcare and life sciences in the UK",
    (
        "Get access to the UK health and life sciences supply-chain, delivering "
        "high quality, innovative services to the world."
    ),
    "Find out more about the UK’s healthcare and life sciences",
]
EXPECTED_STRINGS_TECHNOLOGY = [
    "The UK's advanced technology",
    (
        "Check out the cutting-edge technological innovations that the UK is "
        "bringing to the world."
    ),
    "Find out more about UK technology",
]
EXPECTED_STRINGS_CREATIVE = [
    "The UK's creative services",
    (
        "Whether you need buildings designed, films made or a fresh approach to "
        "marketing, the UK is the first place to look."
    ),
    "Find out more about the UK’s creative services",
]
EXPECTED_STRINGS_FOOD_AND_DRINK = [
    "The UK's food and drink",
    (
        "Whether you want the best food brands or exceptional quality drinks, the"
        " UK should be first on your list."
    ),
    "Find out more about UK food and drink",
]


def go_to(session: Session) -> Response:
    headers = {"Referer": get_absolute_url("ui-supplier:landing")}
    return make_request(Method.GET, URL, session=session, headers=headers)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on FAS Industries page")


def should_see_industry_section(response: Response, industry: str):
    if industry == "health":
        expected = EXPECTED_STRINGS_HEALTH
    elif industry == "technology":
        expected = EXPECTED_STRINGS_TECHNOLOGY
    elif industry == "creative":
        expected = EXPECTED_STRINGS_CREATIVE
    elif industry == "food and drink":
        expected = EXPECTED_STRINGS_FOOD_AND_DRINK
    else:
        raise KeyError("Couldn't recognize '{}' as industry".format(industry))
    check_response(response, 200, body_contains=expected)
