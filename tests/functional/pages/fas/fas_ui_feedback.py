# -*- coding: utf-8 -*-
"""FAS - Edit Company's Directory Profile page"""
import logging

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.pages import Services
from tests.functional.utils.context_utils import Feedback
from tests.functional.utils.generic import assert_that_captcha_is_in_dev_mode
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Services.FAS
NAME = "Feedback"
TYPE = "form"
URL = get_absolute_url("ui-supplier:feedback")
EXPECTED_STRINGS_FORM = [
    "Get UK companies to fulfil your business needs",
    (
        "Tell us what kind of goods or services you need. We'll put you in touch "
        "with relevant UK suppliers."
    ),
    "Your name",
    "Email address",
    "Organisation name",
    "Country",
    "Describe what you need",
    "Maximum 1000 characters.",
    "I agree to the great.gov.uk terms and conditions",
    "Send",
]
EXPECTED_STRINGS_SUCCESSFUL_SUBMISSION = [
    "Your request has been submitted",
    "Thank you for letting us know about your organisation’s needs.",
    (
        "UK government staff based in your region will be in touch to let you "
        "know how UK businesses can help you."
    ),
]
EXPECTED_STRINGS_ERRORS = [
    "This field is required.",
    "Tick the box to confirm you agree to the terms and conditions.",
]


def go_to(session: Session) -> Response:
    headers = {"Referer": get_absolute_url("ui-supplier:feedback")}
    return make_request(Method.GET, URL, session=session, headers=headers)


def should_be_here(response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS_FORM)
    logging.debug("Buyer is on FAS send Feedback page")


def should_see_feedback_submission_confirmation(response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS_SUCCESSFUL_SUBMISSION)
    logging.debug("Feedback submission was confirmed.")


def should_see_errors(response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS_ERRORS)
    logging.debug("Buyer was presented with Feedback submission errors.")


def submit(session: Session, feedback: Feedback, *, referer: str = None) -> Response:
    """Submit feedback form.

    :param feedback: a namedtuple with Feedback request details
    :param referer: (optional) Originating page. Defaults to "{FAS}/feedback"
    """
    assert_that_captcha_is_in_dev_mode(go_to, session)
    if referer:
        headers = {"Referer": referer}
    else:
        headers = {"Referer": get_absolute_url("ui-supplier:feedback")}

    data = {
        "full_name": feedback.name,
        "email_address": feedback.email,
        "company_name": feedback.company_name,
        "country": feedback.country,
        "comment": feedback.comment,
        "terms": feedback.terms,
        "g-recaptcha-response": feedback.g_recaptcha_response,
    }
    return make_request(
        Method.POST, URL, session=session, headers=headers, data=data, trim=False
    )
