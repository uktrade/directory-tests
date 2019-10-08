# -*- coding: utf-8 -*-
"""Profile - Request to verify profile"""

from requests import Response

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.context_utils import Actor
from tests.functional.utils.request import (
    Method,
    check_response,
    check_url,
    make_request,
)

SERVICE = Service.PROFILE
NAME = "Request to verify"
TYPE = PageType.CONFIRMATION
URL = URLs.PROFILE_ENROL_NON_CH_REQUEST_TO_VERIFY.absolute
EXPECTED_STRINGS = [
    "To publish your Business Profile, we need to make sure you represent this business",
    "To verify your Business Profile we'll need a copy of your company",
    "VAT certificate",
    "Indemnity insurance",
    "Bank, building society or credit card statement",
]


def should_be_here(response: Response):
    check_url(response, URL)
    check_response(response, 200, body_contains=EXPECTED_STRINGS)


def submit(actor: Actor) -> Response:
    session = actor.session
    data = {}
    return make_request(
        Method.POST,
        URL,
        session=session,
        files=data,
        no_filename_in_multipart_form_data=True,
    )
