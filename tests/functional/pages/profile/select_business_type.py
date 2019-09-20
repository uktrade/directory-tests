# -*- coding: utf-8 -*-
"""Profile - Select Business Type"""
from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.context_utils import Actor, Company
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


def go_to(session: Session) -> Response:
    return make_request(Method.GET, URL, session=session)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)


def submit(actor: Actor, company: Company) -> Response:
    session = actor.session
    headers = {"Referer": URL}
    assert company.business_type
    data = {
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "choice": company.business_type,
    }

    return make_request(Method.POST, URL, session=session, headers=headers, data=data)
