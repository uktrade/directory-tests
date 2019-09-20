# -*- coding: utf-8 -*-
"""SSO - SUD (Profile) Selling Online Overseas page"""
import logging

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Service.PROFILE
NAME = "Selling Online Overseas"
TYPE = PageType.LANDING
URL = URLs.PROFILE_SOO.absolute
EXPECTED_STRINGS = [
    "Account",
    "You are signed in as",
    "Export opportunities",
    "Business profile",
    "Selling online overseas",
    "Selling online overseas",
    (
        "We've built partnerships across the globe with online marketplaces, so "
        "we can fast track your applications and give you access to exclusive "
        "offers."
    ),
    "Selling online overseas (SOO) will help you to:",
    "join online marketplaces around the world",
    "quickly compare and contrast marketplaces",
    "understand what marketplaces need from new applicants to be able to join",
    "understand if a marketplace is a good match for your business",
    "Find marketplaces",
]


def go_to(session: Session) -> Response:
    return make_request(Method.GET, URL, session=session)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the SUD (Profile) Selling Online Overseas page")
