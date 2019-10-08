# -*- coding: utf-8 -*-
"""Profile - Select Business Type"""
from requests import Response, Session

from directory_tests_shared import BusinessType, PageType, Service, URLs
from tests.functional.utils.context_utils import Actor
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Service.PROFILE
NAME = "Select business type"
TYPE = PageType.FORM
URL = URLs.PROFILE_ENROL_SELECT_BUSINESS_TYPE.absolute
EXPECTED_STRINGS = [
    "Select your business type",
    "My business is registered with Companies House",
    "I'm a sole trader or I represent another type of UK ",
    "I'm a UK taxpayer but do not represent a business",
    "My business or organisation is not registered in the UK",
]

BUSINESS_TYPES = {
    BusinessType.COMPANIES_HOUSE: "companies-house-company",
    BusinessType.SOLE_TRADER: "non-companies-house-company",
    BusinessType.CHARITY: "non-companies-house-company",
    BusinessType.PARTNERSHIP: "non-companies-house-company",
    BusinessType.OTHER: "non-companies-house-company",
    BusinessType.INDIVIDUAL: "not-company",
    BusinessType.OVERSEAS_COMPANY: "overseas-company",
}


def go_to(session: Session) -> Response:
    headers = {
        "Referer": f"{URLs.PROFILE_ENROL.absolute}?next={URLs.DOMESTIC_LANDING_UK.absolute}"
    }
    return make_request(Method.GET, URL, headers=headers, session=session)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)


def submit(actor: Actor, business_type: BusinessType) -> Response:
    session = actor.session
    headers = {"Referer": URLs.PROFILE_ENROL_SELECT_BUSINESS_TYPE.absolute}
    data = {
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "choice": BUSINESS_TYPES[business_type],
    }

    return make_request(
        Method.POST,
        URL,
        session=session,
        headers=headers,
        files=data,
        no_filename_in_multipart_form_data=True,
    )
