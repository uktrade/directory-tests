# -*- coding: utf-8 -*-
"""Profile - Edit Company's products and services industry"""

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.request import (
    Method,
    check_response,
    check_url,
    make_request,
)

SERVICE = Service.PROFILE
NAME = "Edit company's products and services (industry)"
TYPE = PageType.FORM
URL = URLs.PROFILE_ADD_PRODUCTS_AND_SERVICES.absolute
EXPECTED_STRINGS = ["Choose the industry you’re in"]


def should_be_here(response: Response):
    check_url(response, URL)
    check_response(response, 200, body_contains=EXPECTED_STRINGS)


def submit(session: Session, industry: str) -> Response:
    headers = {"Referer": URL}
    data = {"choice": industry}
    return make_request(Method.POST, URL, session=session, headers=headers, data=data)
