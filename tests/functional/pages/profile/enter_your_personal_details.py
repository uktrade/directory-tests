# -*- coding: utf-8 -*-
"""Profile - Enter your personal details"""

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.context_utils import Actor
from tests.functional.utils.request import (
    Method,
    check_response,
    check_url,
    make_request,
)

SERVICE = Service.PROFILE
NAME = "Enter your personal details"
TYPE = PageType.FORM
URL = URLs.PROFILE_ENROL_PERSONAL_DETAILS.absolute
EXPECTED_STRINGS = ["Enter your personal details"]


def go_to(session: Session) -> Response:
    return make_request(Method.GET, URL, session=session)


def should_be_here(response: Response):
    check_url(response, URL)
    check_response(response, 200, body_contains=EXPECTED_STRINGS)


def submit(actor: Actor, *, tick_t_and_c: bool = False):
    session = actor.session
    headers = {"Referer": URL}
    data = {
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "companies_house_enrolment_view-current_step": "personal-details",
        "personal-details-given_name": "AUTOMATED",
        "personal-details-family_name": "TESTS",
        "personal-details-job_title": "AUTOMATED TESTS",
        "personal-details-phone_number": "0987654321",
        "personal-details-confirmed_is_company_representative": "on",
    }
    if tick_t_and_c:
        data.update({"personal-details-terms_agreed": "on"})

    return make_request(
        Method.POST,
        URL,
        session=session,
        headers=headers,
        files=data,
        no_filename_in_multipart_form_data=True,
    )
