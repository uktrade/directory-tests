# -*- coding: utf-8 -*-
"""FAB - Add Case Study - Basic page"""
import logging
from urllib.parse import urljoin

from requests import Response, Session
from tests import get_absolute_url
from tests.functional.utils.context_utils import CaseStudy
from tests.functional.utils.request import Method, check_response, make_request

URL = get_absolute_url("ui-buyer:case-study-create")
EDIT_URL = get_absolute_url("ui-buyer:case-study-edit")
EXPECTED_STRINGS = [
    "Create case study or project", "Basic", "Images",
    ("Describe something significant your company has done that will be "
     "relevant to international buyers. For example, you could add details of "
     "a significant collaboration on a recent international project or a major "
     "export deal."), "Title of your case study or project:",
    "Give your case study a title of 60 characters or fewer.",
    "Summary of your case study or project:",
    ("Summarise your case study in 200 characters or fewer. This will appear "
     "on your main trade profile page"), "Describe your case study or project:",
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


def should_be_here(response: Response):
    """Check if User is on the correct page.

    :param response: response object
    """
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on 'Create case study or project' - basic page")


def go_to(session: Session, *, case_number: int = None) -> Response:
    """Go to "Add Case Study" basic - page.

    This requires:
     * Supplier to be logged in

    :param session: Supplier session object
    :param case_number: (optional) case study number
    """
    if case_number:
        url = urljoin(EDIT_URL, str(case_number), "/")
    else:
        url = URL
    headers = {"Referer": get_absolute_url("ui-buyer:company-profile")}
    response = make_request(Method.GET, url, session=session, headers=headers)
    logging.debug("Supplier is on the Add Case Study - Basic page")
    return response


def prepare_form_data(token: str, case_study: CaseStudy) -> dict:
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


def submit_form(session: Session, token: str, case_study: CaseStudy) -> Response:
    """Submit the form with basic case study data.

    :param session: Supplier session object
    :param token: CSRF token required to submit the form
    :param case_study: a CaseStudy namedtuple with random data
    """
    data = prepare_form_data(token, case_study)
    headers = {"Referer": URL}
    response = make_request(
        Method.POST, URL, session=session, headers=headers, data=data)
    logging.debug(
        "Supplier successfully submitted basic case study data: %s", data)
    return response
