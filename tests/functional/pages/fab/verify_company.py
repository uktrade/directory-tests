# -*- coding: utf-8 -*-
"""Find a Buyer - Verify Company page"""
import logging

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Service.FAB
NAME = "Verify company"
TYPE = PageType.FORM
URL = URLs.FAB_CONFIRM_COMPANY_ADDRESS.absolute
EXPECTED_STRINGS = [
    "Verify your company",
    "Enter the 12 digit code from the letter that was sent to",
    "Sign in with Companies House",
    "Alternatively you can sign in to Companies House to verify",
    (
        "You will need your Companies House authentication code and the email and"
        " password you use to sign in"
    ),
]

EXPECTED_STRINGS_VERIFIED = [
    "Your company has been verified",
    "View or amend your company profile",
    URLs.FAB_COMPANY_PROFILE.relative,
]


def go_to(session: Session, *, referer: str = None) -> Response:
    referer = referer or URLs.PROFILE_BUSINESS_PROFILE.absolute
    headers = {"Referer": referer}
    return make_request(Method.GET, URL, session=session, headers=headers)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on the Verify Company page")


def submit(
    session: Session, token: str, verification_code: str, *, referer: str = None
) -> Response:
    """Submit the form with verification code."""
    if referer is None:
        referer = URLs.PROFILE_BUSINESS_PROFILE.absolute
    headers = {"Referer": referer}
    data = {
        "csrfmiddlewaretoken": token,
        "company_address_verification_view-current_step": "address",
        "address-code": verification_code,
    }
    return make_request(Method.POST, URL, session=session, headers=headers, data=data)


def should_see_company_is_verified(response: Response):
    """Check is Supplier was told that the company has been verified"""
    check_response(response, 200, body_contains=EXPECTED_STRINGS_VERIFIED)
    logging.debug("Supplier is on the Verify Company page")
