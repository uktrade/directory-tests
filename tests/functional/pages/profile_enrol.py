# -*- coding: utf-8 -*-
"""Profile - Enrol - Create an account"""

from requests import Response, Session
from tests import get_absolute_url
from tests.functional.utils.request import Method, check_response, make_request

URL = get_absolute_url("profile:enrol")
EXPECTED_STRINGS = [
    "Create an account",
]


def go_to(session: Session) -> Response:
    return make_request(Method.GET, URL, session=session)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
