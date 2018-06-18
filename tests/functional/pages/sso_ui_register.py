# -*- coding: utf-8 -*-
"""SSO - Registration page"""
import logging
from urllib.parse import quote, urljoin

from requests import Response, Session
from tests import get_absolute_url
from tests.functional.utils.context_utils import Actor, Company
from tests.functional.utils.request import Method, check_response, make_request

URL = get_absolute_url("sso:signup")
EXPECTED_STRINGS = [
    "Register", "Create a great.gov.uk account and you can",
    "save your progress as you read through our exporting guidance",
    "create a free trade profile to promote your company to overseas buyers",
    "express your interest and apply for export opportunities",
    "Email:", "Confirm email:", "Password:", "Confirm password:",
    "Your password must:", "be at least 10 characters",
    "contain at least one letter", "contain at least one number",
    'not contain the word "password"',
    "Tick this box to accept the", "terms and conditions",
    "of the great.gov.uk service."
]


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the SSO Registration page")


def go_to(
        session: Session, *, next: str = None, referer: str = None)\
        -> Response:
    referer = referer or get_absolute_url("ui-buyer:landing")
    if next:
        url = urljoin(URL, "?next={}".format(next))
    else:
        url = URL
    headers = {"Referer": referer}
    response = make_request(
        Method.GET, url, session=session, headers=headers)
    return response


def submit(actor: Actor, company: Company, exported: bool) -> Response:
    """Will submit the SSO Registration form with Supplier & Company details.

    :param actor: a namedtuple with Actor details
    :param company: a namedtuple with Company details
    :param exported: True is exported in the past, False if not
    """
    session = actor.session
    next_url = get_absolute_url("ui-buyer:register-submit-account-details")
    next_link_query = ("?company_number={}&has_exported_before={}"
                       .format(company.number, exported))
    next_link = quote(urljoin(next_url, next_link_query))
    referer_query = "?next={}".format(next_link)
    headers = {"Referer": urljoin(URL, referer_query)}
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


def submit_no_company(
        actor: Actor, *, next: str = None, referer: str = URL) -> Response:
    """Will submit the SSO Registration form without company's details.

    Used when Supplier creates a SSO/great.gov.uk account first.
    """
    session = actor.session
    headers = {"Referer": referer}
    data = {
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "email": actor.email,
        "email2": actor.email,
        "password1": actor.password,
        "password2": actor.password,
        "terms_agreed": "on",
    }
    if next:
        data["next"] = next

    response = make_request(
        Method.POST, URL, session=session, headers=headers, data=data)

    return response
