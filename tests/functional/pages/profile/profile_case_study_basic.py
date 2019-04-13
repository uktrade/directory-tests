# -*- coding: utf-8 -*-
"""Profile - Add Case Study - Basics details page"""
import logging

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.pages import Services
from tests.functional.utils.context_utils import CaseStudy
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Services.PROFILE
NAME = "Add case study (basic details)"
TYPE = "form"
URL = get_absolute_url("profile:case-study-details")
EDIT_URL = get_absolute_url("profile:case-study-edit")
EXPECTED_STRINGS = [
    "Business showcase",
    "Showcase title",
]


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on 'Create case study or project' - basic page")


def go_to(session: Session, *, case_number: int = None) -> Response:
    """Go to "Add Case Study" basic - page.

    This requires:
     * Supplier to be logged in
    """
    if case_number:
        url = EDIT_URL.format(case_number=case_number)
    else:
        url = URL
    headers = {"Referer": get_absolute_url("ui-buyer:company-profile")}
    response = make_request(Method.GET, url, session=session, headers=headers)
    logging.debug("Supplier is on the Add Case Study - Basic page")
    return response


def prepare_form_data(token: str, case_study: CaseStudy) -> dict:
    """Prepare form data based on the flags and custom values provided."""
    data = {
        "csrfmiddlewaretoken": token,
        "case_study_wizard_create_view-current_step": "details",
        "details-title": case_study.title,
        "details-short_summary": case_study.summary,
        "details-description": case_study.description,
        "details-sector": case_study.sector,
        "details-website": case_study.website,
        "details-keywords": case_study.keywords,
    }
    return data


def submit(session: Session, token: str, case_study: CaseStudy) -> Response:
    """Submit the form with basic case study data."""
    data = prepare_form_data(token, case_study)
    headers = {"Referer": URL}
    response = make_request(
        Method.POST, URL, session=session, headers=headers, data=data
    )
    logging.debug(
        "Supplier successfully submitted basic case study data: %s", data
    )
    return response
