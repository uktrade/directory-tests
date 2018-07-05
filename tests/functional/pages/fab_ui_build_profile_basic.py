# -*- coding: utf-8 -*-
"""FAB - Build and improve your profile page"""
import logging

from requests import Response, Session
from tests import get_absolute_url
from tests.functional.utils.context_utils import Actor, Company
from tests.functional.utils.request import Method, check_response, make_request

URL = get_absolute_url("ui-buyer:company-edit")
EXPECTED_STRINGS = [
    "Create your business profile",
    ("Enter your company name and contact details, then select the industry or"
     " industries you work in"),
    ("Add extra information and your company logo to complete your profile. "
     "You can come back and edit your profile at any time."),
    "Your company details",
    "Company name", "Website (optional)", "Enter your trading name",
    "The website address must start with either http:// or https://",
    "Enter up to 10 keywords that describe your company (separated by commas)",
    ("These keywords will be used to help potential overseas buyers find your "
     "company."), "How many employees are in your company?", "Next",
    ("Tell international buyers more about your business to ensure the right "
     "buyers can find you.")
]


def go_to(session: Session) -> Response:
    return make_request(Method.GET, URL, session=session)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the FAB Build and improve your profile")


def submit(actor: Actor, company: Company) -> Response:
    """Submit Build your profile - Basic details form."""
    data = {
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "company_profile_edit_view-current_step": "basic"
    }
    if company.title is not None:
        data.update({"basic-name": company.title})
    if company.website is not None:
        data.update({"basic-website": company.website})
    if company.keywords is not None:
        data.update({"basic-keywords": company.keywords})
    if company.no_employees is not None:
        data.update({"basic-employees": company.no_employees})
    headers = {"Referer": URL}
    return make_request(
        Method.POST, URL, session=actor.session, headers=headers, data=data)
