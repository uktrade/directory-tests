# -*- coding: utf-8 -*-
"""Profile - Publish Company's Business Profile to FAS"""
from requests import Response, Session
from tests import get_absolute_url
from tests.functional.utils.request import Method, make_request

URL = get_absolute_url("profile:publish-business-profile-to-fas")


def submit(session: Session) -> Response:
    """Submit the form with verification code."""
    headers = {"Referer": URL}
    data = {
        "is_published_find_a_supplier": "on"
    }
    return make_request(
        Method.POST, URL, session=session, headers=headers, data=data
    )
