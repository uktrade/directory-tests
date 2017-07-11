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


def prepare_form_data(
        context, supplier_alias, *, current_case_no=None,
        new_title=True, new_summary=True, new_description=True, new_sector=True,
        new_website=True, new_keywords=True,
        custom_title=None, custom_summary=None, custom_description=None,
        custom_sector=None, custom_website=None, custom_keywords=None):
    """Prepare form data based on the flags and custom values provided.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :param current_case_no: number of current study case stored in scenario data
                            Will use empty one if not provided.
    :param new_title: update title if True, or use the current one if False
    :param new_summary: update summary if True, or use the current one if False
    :param new_description: update description if True, or use the current one if False
    :param new_sector: update sector if True, or use the current one if False
    :param new_website: update website if True, or use the current one if False
    :param new_keywords: update keywords if True, or use the current one if False
    :param custom_title: use specific case study title (if provided)
    :param custom_summary: use specific case study summary (if provided)
    :param custom_description: use specific case study description (if provided)
    :param custom_sector: use specific case study sector (if provided)
    :param custom_website: use specific case study website (if provided)
    :param custom_keywords: use specific case study keywords (if provided)
    """
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    token = actor.csrfmiddlewaretoken
    c = company.case_studies.get(current_case_no, CaseStudy())

    fake_title = FAKE.sentence()
    fake_summary = FAKE.sentence()
    fake_description = FAKE.sentence()
    rand_sector = random.choice(SECTORS)
    fake_website = "http://{}/fake-case-study-url".format(FAKE.domain_name())
    rand_keywords = ", ".join(FAKE.sentence().replace(".", "").split())

    title = custom_title or fake_title if new_title else c.title
    summary = custom_summary or fake_summary if new_summary else c.summary
    description = custom_description or fake_description if new_description else c.description
    sector = custom_sector or rand_sector if new_sector else c.sector
    website = custom_website or fake_website if new_website else c.website
    keywords = custom_keywords or rand_keywords if new_keywords else c.keywords

    data = {
        "csrfmiddlewaretoken": token,
        "supplier_case_study_wizard_view-current_step": "basic",
        "basic-title": title,
        "basic-short_summary": summary,
        "basic-description": description,
        "basic-sector": sector,
        "basic-website": website,
        "basic-keywords": keywords
    }

    return data


def submit_form(context, supplier_alias):
    """Submit the form with basic case study data.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session

    data = prepare_form_data(context, supplier_alias)
    headers = {"Referer": URL}
    response = make_request(Method.POST, URL, session=session, headers=headers,
                            data=data, allow_redirects=False, context=context)

    fab_ui_case_study_images.should_be_here(response)
    extract_and_set_csrf_middleware_token(context, response, supplier_alias)
    logging.debug("%s successfully submitted basic case study details: %s",
                  supplier_alias, data)
