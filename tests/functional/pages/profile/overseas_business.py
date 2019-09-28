# -*- coding: utf-8 -*-
"""Profile - Overseas business cannot create an account"""

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.request import (
    Method,
    check_response,
    check_url,
    make_request,
)

NAME = "Overseas business cannot create an account"
SERVICE = Service.PROFILE
TYPE = PageType.CONTENT
URL = URLs.PROFILE_ENROL_OVERSEAS_BUSINESS.absolute
EXPECTED_STRINGS = ["You cannot create an account", "Back"]


def go_to(session: Session) -> Response:
    return make_request(Method.GET, URL, session=session)


def should_be_here(response: Response):
    check_url(response, URL)
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
