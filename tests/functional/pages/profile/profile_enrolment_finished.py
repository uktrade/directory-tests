# -*- coding: utf-8 -*-
"""Profile - Enrolment finished"""

from requests import Response, Session
from tests import get_absolute_url
from tests.functional.utils.request import Method, check_response, make_request

URL = get_absolute_url("profile:enrol-finished")
EXPECTED_STRINGS = [
    "Your account has been created",
]


def go_to(session: Session) -> Response:
    return make_request(Method.GET, URL, session=session)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
