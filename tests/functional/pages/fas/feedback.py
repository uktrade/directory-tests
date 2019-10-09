# -*- coding: utf-8 -*-
"""Find a Supplier - Edit Company's Directory Profile page"""
import logging

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.context_utils import Actor, Feedback
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Service.FAS
NAME = "Feedback"
TYPE = PageType.FORM
URL = URLs.CONTACT_US_FEEDBACK.absolute
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
    "We have received your enquiry",
    "also sent an email with the information",
    "What happens next",
]
EXPECTED_STRINGS_ERRORS = [
    "This field is required.",
    "Tick the box to confirm you agree to the terms and conditions.",
]


def go_to(session: Session) -> Response:
    headers = {"Referer": URL}
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


def submit(actor: Actor, feedback: Feedback, *, referer: str = None) -> Response:
    """Submit feedback form.

    :param feedback: a namedtuple with Feedback request details
    :param referer: (optional) Originating page. Defaults to "{FAS}/feedback"
    """
    session = actor.session
    if referer:
        headers = {"Referer": referer}
    else:
        headers = {"Referer": URL}

    data = {
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "name": feedback.name,
        "email": feedback.email,
        "comment": feedback.comment,
        "terms_agreed": feedback.terms,
        "g-recaptcha-response": feedback.g_recaptcha_response,
    }
    return make_request(
        Method.POST, URL, session=session, headers=headers, data=data, trim=False
    )
