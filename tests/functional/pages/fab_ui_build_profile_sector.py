# -*- coding: utf-8 -*-
"""FAB - Build and improve your profile page"""
import logging

from requests import Response
from tests import get_absolute_url
from tests.functional.utils.context_utils import Actor
from tests.functional.utils.request import Method, check_response, make_request
from tests.settings import SECTORS

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
    "Save",
] + SECTORS


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug(
        "Successfully got to the FAB Build and improve your profile. Choose "
        "Your company sector"
    )


def submit(actor: Actor, sector: str, countries: list, other: str) -> Response:
    """Submit Build your profile - Choose your sector form."""
    headers = {"Referer": URL}
    data = {
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "company_profile_edit_view-current_step": "classification",
        "classification-sectors": sector,
        "classification-export_destinations": countries,
        "classification-export_destinations_other": other,
    }
    response = make_request(
        Method.POST, URL, session=actor.session, headers=headers, data=data
    )
    return response
