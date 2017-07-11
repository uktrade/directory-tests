# -*- coding: utf-8 -*-
"""FAB - Add Case Study - Basic page"""
import logging
import random

from faker import Factory

from tests import get_absolute_url
from tests.functional.features.context_utils import CaseStudy
from tests.functional.features.pages import fab_ui_case_study_images
from tests.functional.features.pages.utils import (
    extract_and_set_csrf_middleware_token
)
from tests.functional.features.utils import Method, check_response, make_request
from tests.settings import SECTORS

URL = get_absolute_url("ui-buyer:case-study-add")
EXPECTED_STRINGS = [
    "Create case study or project", "Basic", "Images",
    ("Describe something significant your company has done that will be "
     "relevant to international buyers. For example, you could add details of "
     "a significant collaboration on a recent international project or a major "
     "export deal."), "Title of your case study or project:",
    "Give your case study a title of 60 characters or fewer.",
    "Summary of your case study or project:",
    ("Summarise your case study in 50 words or fewer. This will appear on your "
     "main trade profile page."), "Describe your case study or project:",
    ("Describe the project or case study in 1,000 characters or fewer. Use this"
     " space to demonstrate the value of your company to an international "
     "business audience."), "Sector:",
    "Select the sector most relevant to your case study or project.",
    "The web address for your case study (optional):",
    "Enter a full URL including http:// or https://",
    ("Enter up to 10 keywords that describe your case study. Keywords should "
     "be separated by commas."),
    ("These keywords will be used to help potential overseas buyers find your "
     "case study."), "Next", "Cancel"
]
FAKE = Factory.create()


def should_be_here(response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on 'Create case study or project' - basic page")


def go_to(context, supplier_alias):
    """Go to "Add Case Study" basic - page.

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
    logging.debug("%s is on the Add Case Study - Basic page", supplier_alias)


def prepare_form_data(token, case_study):
    """Prepare form data based on the flags and custom values provided.

    :param token: CSRF middleware token required to submit the form
    :param case_study: a CaseStudy namedtuple with random data
    :return: form data with all fields filled out
    """
    data = {
        "csrfmiddlewaretoken": token,
        "supplier_case_study_wizard_view-current_step": "basic",
        "basic-title": case_study.title,
        "basic-short_summary": case_study.summary,
        "basic-description": case_study.description,
        "basic-sector": case_study.sector,
        "basic-website": case_study.website,
        "basic-keywords": case_study.keywords
    }

    return data


def submit_form(context, supplier_alias, case_study):
    """Submit the form with basic case study data.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :param case_study: a CaseStudy namedtuple with random data
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session
    token = actor.csrfmiddlewaretoken
    data = prepare_form_data(token, case_study)
    headers = {"Referer": URL}

    response = make_request(Method.POST, URL, session=session, headers=headers,
                            data=data, allow_redirects=False, context=context)
    logging.debug("%s successfully submitted basic case study details: %s",
                  supplier_alias, data)
    return response
