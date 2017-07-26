# -*- coding: utf-8 -*-
"""FAB - Build and improve your profile page"""
import logging

from requests import Response

from tests import get_absolute_url
from tests.functional.features.context_utils import Actor
from tests.functional.features.utils import Method, check_response, make_request
from tests.settings import SECTORS

URL = get_absolute_url("ui-buyer:company-edit")
EXPECTED_STRINGS = [
    "Your company sector", "Basic", "Industry and exporting", "Address",
    "Confirm",
    "What industry is your company in?",
    "< Back to previous step", "Next", "Select the countries you would like to export to:",
    "China", "Germany", "India", "Japan", "United States", "Other", "Enter 3 maximum"
] + SECTORS


def should_be_here(response: Response):
    """Check if Supplier is on FAB Build and improve your profile page.

    :param response: response object
    """
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the FAB Build and improve your profile. "
                  "Choose Your company sector")


def submit(actor: Actor, sector: str, country: str, other: str) -> Response:
    """Submit Build your profile - Choose your sector form.

    :param actor: a namedtuple with Actor details
    :param sector: Industry Sector in which company is interested in
    :param country: country code of the country you're exporting to
    :param other: list of other countries your company is exporting to
    :return: response object
    """
    headers = {"Referer": URL}
    data = {
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "company_profile_edit_view-current_step": "classification",
        "classification-sectors": sector,
        "classification-export_destinations": country,
        "classification-export_destinations_other": other
    }
    response = make_request(
        Method.POST, URL, session=actor.session, headers=headers, data=data)
    return response
