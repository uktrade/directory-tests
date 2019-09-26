# -*- coding: utf-8 -*-
"""Profile - Edit Company's Description page"""
import logging

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Service.PROFILE
NAME = "Edit company's description"
TYPE = PageType.FORM
URL = URLs.PROFILE_EDIT_COMPANY_DESCRIPTION.absolute
EXPECTED_STRINGS = [
    "Company description",
    "Describe your business to overseas buyers",
    "Brief summary to make your company stand out to buyers",
]


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on the Select Sector page")


def go_to(session: Session) -> Response:
    headers = {"Referer": URLs.PROFILE_BUSINESS_PROFILE.absolute}
    return make_request(Method.GET, URL, session=session, headers=headers)


def submit(session: Session, summary: str, description: str) -> Response:
    headers = {"Referer": URL}
    data = {"summary": summary, "description": description}
    return make_request(Method.POST, URL, session=session, headers=headers, data=data)
