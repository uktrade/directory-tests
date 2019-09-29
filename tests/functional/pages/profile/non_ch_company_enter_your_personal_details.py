# -*- coding: utf-8 -*-
"""Profile - Non Companies House company Enter your personal details"""

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
NAME = "Non Companies House company enter your personal details"
TYPE = PageType.FORM
URL = URLs.PROFILE_ENROL_NON_CH_COMPANY_ENTER_PERSONAL_DETAILS.absolute
EXPECTED_STRINGS = [
    "Enter your personal details",
    "First name",
    "Last name",
    "Job title",
    "Phone number (optional)",
]


def should_be_here(response: Response):
    check_url(response, URL)
    check_response(response, 200, body_contains=EXPECTED_STRINGS)


def submit(actor: Actor):
    session = actor.session
    headers = {"Referer": URL}
    data = {
        "non_companies_house_enrolment_view-current_step": "personal-details",
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "personal-details-given_name": "AUTOMATED",
        "personal-details-family_name": "TESTS",
        "personal-details-job_title": "AUTOMATED TESTS",
        "personal-details-phone_number:": "0987654321",
        "personal-details-confirmed_is_company_representative": "on",
    }

    return make_request(Method.POST, URL, session=session, headers=headers, data=data)
