# -*- coding: utf-8 -*-
"""SSO - Registration page"""
import logging
from urllib.parse import quote

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.features.context_utils import Actor, Company
from tests.functional.features.utils import Method, check_response, make_request

URL = get_absolute_url("sso:signup")
EXPECTED_STRINGS = [
    "Register", "Create a great.gov.uk account and you can",
    "gain access to worldwide exporting opportunities",
    "promote your business to international buyers",
    "Email:", "Confirm email:", "Password:", "Confirm password:",
    "Tick this box to accept the", "terms and conditions",
    "of the great.gov.uk service."
]


def should_be_here(response: Response):
    """Check if Supplier is on SSO Registration Page.

    :param response: response object
    """
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the SSO Registration page")


def go_to(session: Session) -> Response:
    """Go to the SSO Registration page.

    :param session: Supplier session object
    :return: response object
    """
    headers = {"Referer": get_absolute_url("ui-buyer:landing")}
    response = make_request(
        Method.GET, URL, session=session, headers=headers)
    should_be_here(response)
    return response


def submit(actor: Actor, company: Company, export_status: str) -> Response:
    """Will submit the SSO Registration form with Supplier & Company details.

    :param actor: a namedtuple with Actor details
    :param company: a namedtuple with Company details
    :param export_status: export status of the company
    """
    session = actor.session
    next_url = get_absolute_url("ui-buyer:register-submit-account-details")
    next_link = quote(
        "{}?company_number={}&export_status={}".format(next_url, company.number,
                                                       export_status))
    headers = {"Referer": "{}?next={}".format(URL, next_link)}
    data = {
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "email": actor.email,
        "email2": actor.email,
        "password1": actor.password,
        "password2": actor.password,
        "terms_agreed": "on",
        "next": next_link
    }

    response = make_request(
        Method.POST, URL, session=session, headers=headers, data=data)

    return response


def submit_no_company(actor: Actor) -> Response:
    """Will submit the SSO Registration form without company's details.

    Used when Supplier creates a SSO/great.gov.uk account first.

    :param actor: a namedtuple with Actor details
    """
    session = actor.session
    headers = {"Referer": URL}
    data = {
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "email": actor.email,
        "email2": actor.email,
        "password1": actor.password,
        "password2": actor.password,
        "terms_agreed": "on",
    }

    response = make_request(
        Method.POST, URL, session=session, headers=headers, data=data)

    return response
