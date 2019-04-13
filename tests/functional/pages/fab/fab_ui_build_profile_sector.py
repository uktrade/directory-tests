# -*- coding: utf-8 -*-
"""FAB - Build and improve your profile page"""
import logging

from requests import Response

from tests import get_absolute_url
from tests.functional.pages import Services
from tests.functional.utils.context_utils import Actor
from tests.functional.utils.request import Method, check_response, make_request
from tests.settings import SECTORS

SERVICE = Services.FAB
NAME = "Build and improve your profile"
TYPE = "form"
URL = get_absolute_url("ui-buyer:company-edit")
EXPECTED_STRINGS = [
    "Your company sector",
    "About your company",
    "Industry and exporting",
    "What industry is your company in?",
    "< Back to previous step",
    "Select the countries you would like to export to:",
    "China",
    "Germany",
    "India",
    "Japan",
    "United States",
    "Other",
    "Enter 3 maximum",
    "Back to previous step",
    "Have you exported before?",
    "Yes",
    "No",
    "Save",
] + SECTORS


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug(
        "Successfully got to the FAB Build and improve your profile. Choose "
        "Your company sector"
    )


def submit(
        actor: Actor, sector: str, countries: list, other: str,
        has_exported_before: bool) -> Response:
    """Submit Build your profile - Choose your sector form."""
    headers = {"Referer": URL}
    data = {
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "company_profile_edit_view-current_step": "classification",
        "classification-sectors": sector,
        "classification-export_destinations": countries,
        "classification-export_destinations_other": other,
        "classification-has_exported_before": has_exported_before,
    }
    response = make_request(
        Method.POST, URL, session=actor.session, headers=headers, data=data
    )
    return response
