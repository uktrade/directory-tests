# -*- coding: utf-8 -*-
"""FAB - Edit Company's Details page"""
import random

from requests import Response, Session
from tests import get_absolute_url
from tests.functional.utils.context_utils import Actor, Company
from tests.functional.utils.generic import (
    Method,
    make_request,
    rare_word,
    sentence
)
from tests.functional.utils.request import check_response
from tests.settings import NO_OF_EMPLOYEES

URL = get_absolute_url("ui-buyer:company-edit-key-facts")
EXPECTED_STRINGS = [
    "Create your trade profile",
    ("Enter your company name and contact details, then select the industry or"
     " industries you work in."),
    "Your company details", "Company name:",
    "Enter your trading name", "Website (optional):",
    "The website address must start with either http:// or https://",
    "Enter up to 10 keywords that describe your company (separated by commas)",
    ("These keywords will be used to help potential overseas buyers find your "
     "company."), "How many employees are in your company?",
    ("Tell international buyers more about your business to ensure the right "
     "buyers can find you.")
] + NO_OF_EMPLOYEES


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)


def go_to(session: Session) -> Response:
    """Go to "Edit Company's Details" page.

    This requires:
     * Supplier to be logged in
    """
    headers = {"Referer": get_absolute_url("ui-buyer:company-profile")}
    response = make_request(Method.GET, URL, session=session, headers=headers)

    should_be_here(response)
    return response


def update_details(
        actor: Actor, company: Company, *, title=True, website=True,
        keywords=True, size=True, specific_title=None, specific_website=None,
        specific_keywords=None, specific_size=None) -> (Response, Company):
    """Update basic Company's details: business name, website, keywords & size.

    Will use random details or specific values if they are provided.
    """
    session = actor.session
    token = actor.csrfmiddlewaretoken

    if title:
        new_title = specific_title or sentence()
    else:
        new_title = company.title

    if website:
        new_website = specific_website or ("http://{}.{}"
                                           .format(rare_word(), rare_word()))
    else:
        new_website = company.website

    if keywords:
        random_keywords = ", ".join(sentence().split())
        new_keywords = specific_keywords or random_keywords
    else:
        new_keywords = company.keywords

    if size:
        new_size = specific_size or random.choice(NO_OF_EMPLOYEES)
    else:
        new_size = company.no_employees

    headers = {"Referer": URL}
    data = {
        "csrfmiddlewaretoken": token,
        "supplier_basic_info_edit_view-current_step": "basic",
        "basic-name": new_title,
        "basic-website": new_website,
        "basic-keywords": new_keywords,
        "basic-employees": new_size
    }

    new_details = Company(
        title=new_title, website=new_website, keywords=new_keywords,
        no_employees=new_size)

    response = make_request(
        Method.POST, URL, session=session, headers=headers, data=data)

    return response, new_details
