# -*- coding: utf-8 -*-
"""Profile - Edit Company's products and services keywords"""

from requests import Response, Session
from tests import get_absolute_url
from tests.functional.utils.request import Method, make_request

URL = get_absolute_url("profile:add-products-and-services-keywords")
EXPECTED_STRINGS = []


def submit(session: Session, keywords: str) -> Response:
    headers = {"Referer": URL}
    data = {
        "keywords": keywords,
    }
    return make_request(
        Method.POST, URL, session=session, headers=headers, data=data
    )
