# -*- coding: utf-8 -*-
"""FAB - Build and improve your profile page"""
import logging

from requests import Response

from tests import get_absolute_url
from tests.functional.features.context_utils import Actor, Company
from tests.functional.features.utils import Method, check_response, make_request

URL = get_absolute_url("ui-buyer:company-edit")
EXPECTED_STRINGS = [
    "Build and improve your profile", "Basic", "Industry and exporting",
    "Confirmation",
    ("To set up your Find a Buyer profile, enter your company’s basic details, "
     "then choose which sectors you’re interested in."),
    ("You can add extra information and a company logo to complete your profile"
     ". You can edit your profile at any time."),
    ("From early 2017, your company profile will be published online and "
     "promoted to international buyers."), "Your company details",
    "Company name", "Website (optional)", "Enter your preferred business name",
    "The website address must start with either http:// or https://",
    "Enter up to 10 keywords that describe your company (separated by commas):",
    ("These keywords will be used to help potential overseas buyers find your "
     "company."), "How many employees are in your company?", "Next",
    ("Tell international buyers more about your business to ensure the right "
     "buyers can find you.")
]


def should_be_here(response: Response):
    """Check if Supplier is on FAB Build and improve your profile page.

    :param response: response object
    """
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the FAB Build and improve your profile")


def submit(actor: Actor, company: Company) -> Response:
    """Submit Build your profile - Basic details form.

    :param actor: a namedtuple with Actor details
    :param company: a namedtuple with Company details
    :return: response object
    """
    data = {
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "company_profile_edit_view-current_step": "basic",
        "basic-name": company.title,
        "basic-website": company.website,
        "basic-keywords": company.keywords,
        "basic-employees": company.no_employees
    }
    headers = {"Referer": URL}
    response = make_request(
        Method.POST, URL, session=actor.session, headers=headers, data=data)
    return response
