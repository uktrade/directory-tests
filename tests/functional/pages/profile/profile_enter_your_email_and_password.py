# -*- coding: utf-8 -*-
"""Profile - Enter your business email address and set a password"""

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.pages import Services
from tests.functional.utils.context_utils import Actor
from tests.functional.utils.generic import assert_that_captcha_is_in_dev_mode
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Services.PROFILE
NAME = "Enter your business email address and set a password"
TYPE = "form"
URL = get_absolute_url("profile:enrol-user-account")
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
    assert_that_captcha_is_in_dev_mode(go_to, session)
    headers = {"Referer": URL}
    data = {
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "companies_house_enrolment_view-current_step": "user-account",
        "user-account-email": actor.email,
        "user-account-password": actor.password,
        "user-account-password_confirmed": actor.password,
        "user-account-terms_agreed": "on",
        "g-recaptcha-response": "test mode",
    }

    return make_request(
        Method.POST, URL, session=session, headers=headers, data=data
    )
