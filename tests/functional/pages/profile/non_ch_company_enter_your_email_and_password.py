# -*- coding: utf-8 -*-
"""Profile - Non Companies House Company Enter your business email address and set a password"""
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
NAME = (
    "Non Companies House company enter your business email address and set a password"
)
TYPE = PageType.FORM
URL = URLs.PROFILE_ENROL_NON_CH_COMPANY_ENTER_USER_NAME_AND_PASSWORD.absolute
EXPECTED_STRINGS = [
    "Enter your business email address and set a password",
    "Your email address",
    "Password",
    "Confirm password",
    "Tick this box to accept the",
]


def go_to(session: Session) -> Response:
    return make_request(Method.GET, URL, session=session)


def should_be_here(response: Response):
    check_url(response, URL)
    check_response(response, 200, body_contains=EXPECTED_STRINGS)


def submit(actor: Actor) -> Response:
    session = actor.session
    headers = {"Referer": URL}
    data = {
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "non_companies_house_enrolment_view-current_step": "user-account",
        "user-account-email": actor.email,
        "user-account-password": actor.password,
        "user-account-password_confirmed": actor.password,
        "user-account-terms_agreed": "on",
        "user-account-remote_password_error": None,
        "g-recaptcha-response": "test mode",
    }

    return make_request(Method.POST, URL, session=session, headers=headers, data=data)
