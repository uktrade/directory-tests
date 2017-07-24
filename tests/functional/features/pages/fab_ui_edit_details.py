# -*- coding: utf-8 -*-
"""FAB - Edit Company's Details page"""
import logging
import random

from faker import Factory

from tests import get_absolute_url
from tests.functional.features.pages import fab_ui_profile
from tests.functional.features.pages.utils import (
    extract_and_set_csrf_middleware_token
)
from tests.functional.features.utils import Method, check_response, make_request
from tests.settings import NO_OF_EMPLOYEES

URL = get_absolute_url("ui-buyer:company-edit-key-facts")
EXPECTED_STRINGS = [
    "Build and improve your profile", "Your company details", "Company name:",
    "Enter your preferred business name", "Website (optional):",
    "The website address must start with either http:// or https://",
    "Enter up to 10 keywords that describe your company (separated by commas):",
    ("These keywords will be used to help potential overseas buyers find your "
     "company."), "How many employees are in your company?",
    ("Tell international buyers more about your business to ensure the right "
     "buyers can find you.")
] + NO_OF_EMPLOYEES
FAKE = Factory.create()


def should_be_here(response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)


def go_to(context, supplier_alias):
    """Go to "Edit Company's Details" page.

    This requires:
     * Supplier to be logged in

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session

    headers = {"Referer": get_absolute_url("ui-buyer:company-profile")}
    response = make_request(Method.GET, URL, session=session, headers=headers,
                            allow_redirects=False, context=context)

    should_be_here(response)
    extract_and_set_csrf_middleware_token(context, response, supplier_alias)
    logging.debug("%s is on the Edit Company Details page", supplier_alias)


def update_details(
        context, supplier_alias, *, title=True, website=True, keywords=True,
        size=True, specific_title=None, specific_website=None,
        specific_keywords=None, specific_size=None):
    """Update basic Company's details: business name, website, keywords & size.

    Will use random details or specific values if they are provided.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :param title: change business title if True, or use the current one if False
    :param website: change website if True, or use the current one if False
    :param keywords: change keywords if True, or use the current one if False
    :param size: change number of employees if True, or use the current one
    :param specific_title: use specific business title (if provided)
    :param specific_website: use specific website (if provided)
    :param specific_keywords: use specific keywords (if provided)
    :param specific_size: use specific number of employees (if provided)
    """
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    session = actor.session
    token = actor.csrfmiddlewaretoken

    if title:
        new_title = specific_title or FAKE.sentence()
    else:
        new_title = company.title

    if website:
        new_website = specific_website or "http://{}".format(FAKE.domain_name())
    else:
        new_website = company.website

    if keywords:
        random_keywords = ", ".join(FAKE.sentence().replace(".", "").split())
        new_keywords = specific_keywords or random_keywords
    else:
        new_keywords = company.keywords

    if size:
        new_size = specific_size or random.choice(NO_OF_EMPLOYEES)
    else:
        new_size = company.no_employees

    headers = {"Referer": URL}
    data = {"csrfmiddlewaretoken": token,
            "supplier_basic_info_edit_view-current_step": "basic",
            "basic-name": new_title,
            "basic-website": new_website,
            "basic-keywords": new_keywords,
            "basic-employees": new_size}

    response = make_request(Method.POST, URL, session=session, headers=headers,
                            data=data, allow_redirects=True, context=context)

    fab_ui_profile.should_be_here(response)
    extract_and_set_csrf_middleware_token(context, response, supplier_alias)

    context.set_company_details(
        company.alias, title=new_title, website=new_website,
        keywords=new_keywords, no_employees=new_size)
    logging.debug("%s successfully updated basic Company's details: "
                  "title=%s, website=%s, keywords=%s, number of employees=%s",
                  supplier_alias, new_title, new_website, new_keywords,
                  new_size)
