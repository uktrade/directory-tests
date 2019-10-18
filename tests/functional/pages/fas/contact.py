# -*- coding: utf-8 -*-
"""Find a Supplier - Contact Supplier page"""
import logging
from urllib.parse import urljoin

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.context_utils import Company, Feedback, Message
from tests.functional.utils.generic import escape_html
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Service.FAS
NAME = "Contact Supplier"
TYPE = PageType.FORM
LANDING = URLs.FAS_LANDING.absolute
URL = urljoin(LANDING, "suppliers/{company_number}/contact/")
EXPECTED_STRINGS = [
    "Send a message to",
    "Enter your details and a brief message about your needs",
    "Given name",
    "Family name",
    "Your organisation name",
    "Country",
    "Your email address",
    "Industry",
    "Enter a subject line for your message",
    "Maximum 200 characters",
    "Enter your message to the UK company",
    "Maximum 1000 characters",
    "Captcha",
    "I agree to the ",
    "great.gov.uk terms and conditions",
    "Send message",
]

EXPECTED_STRINGS_MESSAGE_SENT = [
    "Message sent",
    "Your message has been sent to",
    "Next steps",
    "Browse more companies",
]


def go_to(session: Session, company_number: str) -> Response:
    full_url = URL.format(company_number=company_number)
    return make_request(Method.GET, full_url, session=session)


def should_be_here(response, *, name=None):
    extra_strings_to_check = [escape_html(name)] if name else EXPECTED_STRINGS
    expected = EXPECTED_STRINGS + extra_strings_to_check
    check_response(response, 200, body_contains=expected)
    logging.debug("Supplier is on FAS Contact Company page")


def submit(session: Session, message: Message or Feedback, company_number: str):
    full_url = URL.format(company_number=company_number)
    headers = {"Referer": URL.format(company_number=company_number)}
    data = {
        "body": message.body,
        "company_name": message.company_name,
        "country": message.country,
        "email_address": message.email_address,
        "family_name": message.family_name,
        "given_name": message.given_name,
        "g-recaptcha-response": message.g_recaptcha_response,
        "sector": message.sector,
        "subject": message.subject,
        "terms": message.terms,
    }
    return make_request(
        Method.POST, full_url, session=session, headers=headers, data=data
    )


def should_see_that_message_has_been_sent(company: Company, response: Response):
    clean_name = escape_html(company.title.replace("  ", " "))
    expected = EXPECTED_STRINGS_MESSAGE_SENT + [clean_name]
    check_response(response, 200, body_contains=expected)
    logging.debug("Buyer was told that the message has been sent")
