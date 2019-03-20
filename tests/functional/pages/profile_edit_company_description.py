# -*- coding: utf-8 -*-
"""Profile - Edit Company's Description page"""
import logging

from requests import Response, Session
from tests import get_absolute_url
from tests.functional.utils.request import Method, check_response, make_request

URL = get_absolute_url("profile:edit-company-description")
EXPECTED_STRINGS = [
    "Company description",
    "Describe your business to overseas buyers",
    "Brief summary to make your company stand out to buyers",
]


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on the Select Sector page")


def go_to(session: Session) -> Response:
    headers = {"Referer": get_absolute_url("ui-buyer:company-profile")}
    return make_request(Method.GET, URL, session=session, headers=headers)


def submit(session: Session, summary: str, description: str) -> Response:
    headers = {"Referer": URL}
    data = {
        "summary": summary,
        "description": description,
    }
    return make_request(
        Method.POST, URL, session=session, headers=headers, data=data
    )
