# -*- coding: utf-8 -*-
"""Profile - Enter your business details"""

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.context_utils import Actor, Company
from tests.functional.utils.request import (
    Method,
    check_response,
    check_url,
    make_request,
)

SERVICE = Service.PROFILE
NAME = "Enter your business details (CH search)"
TYPE = PageType.FORM
URL = URLs.PROFILE_ENROL_COMPANIES_HOUSE_SEARCH.absolute
EXPECTED_STRINGS = ["Enter your business details"]
UNEXPECTED_STRINGS = ["Invalid code"]


def go_to(session: Session) -> Response:
    return make_request(Method.GET, URL, session=session)


def should_be_here(response: Response):
    check_url(response, URL)
    check_response(
        response,
        200,
        body_contains=EXPECTED_STRINGS,
        unexpected_strings=UNEXPECTED_STRINGS,
    )


def submit(actor: Actor, company: Company) -> Response:
    session = actor.session
    headers = {"Referer": URL}
    data = {
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "companies_house_enrolment_view-current_step": "company-search",
        "company-search-company_name": company.title,
        "company-search-company_number": company.number,
    }

    return make_request(
        Method.POST,
        URL,
        session=session,
        headers=headers,
        files=data,
        no_filename_in_multipart_form_data=True,
    )
