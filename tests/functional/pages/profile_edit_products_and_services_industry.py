# -*- coding: utf-8 -*-
"""Profile - Edit Company's products and services industry"""

from requests import Response, Session
from tests import get_absolute_url
from tests.functional.utils.request import (
    Method,
    make_request,
    check_url,
    check_response,
)

URL = get_absolute_url("profile:add-products-and-services")
EXPECTED_STRINGS = [
    "Choose the products and services industry"
]


def should_be_here(response: Response):
    check_url(response, URL)
    check_response(response, 200, body_contains=EXPECTED_STRINGS)


def submit(session: Session, industry: str) -> Response:
    headers = {"Referer": URL}
    data = {
        "choice": industry,
    }
    return make_request(
        Method.POST, URL, session=session, headers=headers, data=data
    )
