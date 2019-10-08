# -*- coding: utf-8 -*-
"""Profile - Enter your business email address and set a password"""

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.context_utils import Actor
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Service.PROFILE
NAME = "Enter your business email address and set a password"
TYPE = PageType.FORM
URL = URLs.PROFILE_ENROL_USER_ACCOUNT.absolute
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
    check_response(response, 200, body_contains=EXPECTED_STRINGS)


def submit(actor: Actor) -> Response:
    session = actor.session
    headers = {"Referer": URL}
    data = {
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "companies_house_enrolment_view-current_step": "user-account",
        "user-account-email": actor.email,
        "user-account-password": actor.password,
        "user-account-password_confirmed": actor.password,
        "user-account-terms_agreed": "on",
        "user-account-remote_password_error": None,
        "g-recaptcha-response": "test mode",
    }

    return make_request(
        Method.POST,
        URL,
        session=session,
        headers=headers,
        files=data,
        no_filename_in_multipart_form_data=True,
    )
