# -*- coding: utf-8 -*-
"""Profile - Enter your business details"""
from requests import Response, Session

from tests import get_absolute_url
from tests.functional.utils.context_utils import Actor, Company
from tests.functional.utils.request import Method, check_response, make_request

URL = get_absolute_url("profile:enrol-business-details")
EXPECTED_STRINGS = [
    "Enter your business details",
]


def go_to(session: Session) -> Response:
    return make_request(Method.GET, URL, session=session)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)


def submit(actor: Actor, company: Company) -> Response:
    session = actor.session
    headers = {"Referer": URL}
    data = {
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "companies_house_enrolment_view-current_step": "business-details",
        "business-details-company_name": company.title,
        "business-details-postal_code": company.companies_house_details["address"]["postal_code"],
        "business-details-sectors": company.sector,
        "business-details-website_address": company.website,
    }

    return make_request(
        Method.POST, URL, session=session, headers=headers, data=data
    )
