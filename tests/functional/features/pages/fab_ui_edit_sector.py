# -*- coding: utf-8 -*-
"""FAB - Edit Company's Sector page"""
import logging
import random

from tests import get_absolute_url
from tests.functional.features.pages import fab_ui_profile
from tests.functional.features.utils import Method, check_response, make_request
from tests.settings import SECTORS, COUNTRIES

URL = get_absolute_url("ui-buyer:company-edit")
EXPECTED_STRINGS = [
    "Your company sector",
    "What industry is your company in?",
    "Back to previous step", "Select the countries you would like to export to:",
    "China", "Germany", "India", "Japan", "United States", "Other", "Save"
] + SECTORS


def should_be_here(response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on the Select Sector page")


def update_sector_and_countries(
        context, supplier_alias, *, update=True, sector_name=None):
    """Change Company's Sector of Interest.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :param update: update Sector if True or use the current one if False
    :param sector_name: use specific Sector.
            Must be one of sectors specified in `tests.settings.SECTORS`
    """
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    session = actor.session
    token = actor.csrfmiddlewaretoken

    if update:
        new_sector = sector_name or random.choice(SECTORS)
    else:
        new_sector = company.sector

    country = COUNTRIES[random.choice(list(COUNTRIES))]
    other = ""
    headers = {"Referer": URL}
    data = {"csrfmiddlewaretoken": token,
            "supplier_classification_edit_view-current_step": "classification",
            "classification-sectors": new_sector,
            "classification-export_destinations": country,
            "classification-export_destinations_other": other
            }

    response = make_request(Method.POST, URL, session=session, headers=headers,
                            data=data, allow_redirects=True, context=context)

    fab_ui_profile.should_be_here(response)
    context.set_company_details(
        company.alias, sector=new_sector, export_to_countries=country)
    logging.debug("%s set Company's Sector of Interest to: %s", supplier_alias,
                  new_sector)
