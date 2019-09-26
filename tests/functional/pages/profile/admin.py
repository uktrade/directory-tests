# -*- coding: utf-8 -*-
"""Profile - Admin"""
from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.generic import Method, make_request
from tests.functional.utils.request import check_response, check_url

SERVICE = Service.PROFILE
NAME = "Remove profile from account"
TYPE = PageType.FORM
URL = URLs.PROFILE_ADMIN.absolute
EXPECTED_STRINGS = [
    "Profile settings",
    "Collaborators",
    "Remove profile from my account",
]


def should_be_here(response: Response):
    check_url(response, URL)
    check_response(response, 200, body_contains=EXPECTED_STRINGS)


def go_to(session: Session) -> Response:
    headers = {"Referer": URLs.PROFILE_ADMIN.absolute}
    return make_request(Method.GET, URL, session=session, headers=headers)
