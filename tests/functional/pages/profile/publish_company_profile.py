# -*- coding: utf-8 -*-
"""Profile - Publish Company's Business Profile to FAS"""
from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.request import Method, make_request

SERVICE = Service.PROFILE
NAME = "Publish company's business profile"
TYPE = PageType.FORM
URL = URLs.PROFILE_PUBLISH_BUSINESS_PROFILE_TO_FAS.absolute
EXPECTED_STRINGS = []


def submit(session: Session, *, unpublish: bool = False) -> Response:
    """Submit the form with verification code."""
    headers = {"Referer": URL}
    data = {"is_published_find_a_supplier": "on"} if not unpublish else {}
    return make_request(
        Method.POST,
        URL,
        session=session,
        headers=headers,
        files=data,
        no_filename_in_multipart_form_data=True,
    )
