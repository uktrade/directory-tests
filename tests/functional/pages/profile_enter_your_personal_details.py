# -*- coding: utf-8 -*-
"""Profile - Enter your details"""

from requests import Response, Session
from tests import get_absolute_url
from tests.functional.utils.context_utils import Actor, Company
from tests.functional.utils.request import Method, check_response, make_request

URL = get_absolute_url("profile:enrol-personal-details")
EXPECTED_STRINGS = [
    "Enter your details",
]


def go_to(session: Session) -> Response:
    return make_request(Method.GET, URL, session=session)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)


def submit(actor: Actor):
    session = actor.session
    headers = {"Referer": URL}
    data = {
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "companies_house_enrolment_view-current_step": "personal-details",
        "personal-details-given_name": "AUTOMATED",
        "personal-details-family_name": "TESTS",
        "personal-details-job_title": "AUTOMATED TESTS",
        "personal-details-phone_number:": "0987654321",
        "personal-details-confirmed_is_company_representative": "on",
    }

    return make_request(
        Method.POST, URL, session=session, headers=headers, data=data
    )
