# -*- coding: utf-8 -*-
"""Profile - Enter your business details"""
import random

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from directory_tests_shared.constants import SECTORS
from tests.functional.utils.context_utils import Actor, Company
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Service.PROFILE
NAME = "Enter your business details (industry & website)"
TYPE = PageType.FORM
URL = URLs.PROFILE_ENROL_BUSINESS_DETAILS.absolute
EXPECTED_STRINGS = ["Enter your business details"]


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
        "business-details-sectors": company.sector or random.choice(SECTORS),
        "business-details-website": company.website,
    }

    return make_request(
        Method.POST,
        URL,
        session=session,
        headers=headers,
        files=data,
        no_filename_in_multipart_form_data=True,
    )
