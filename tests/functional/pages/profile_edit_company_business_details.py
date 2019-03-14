# -*- coding: utf-8 -*-
"""Profile - Edit Company's business details"""
import random

from directory_constants.constants import choices
from requests import Response
from tests import get_absolute_url
from tests.functional.utils.context_utils import Actor, Company
from tests.functional.utils.generic import (
    Method,
    make_request,
    rare_word,
    sentence,
)
from tests.settings import NO_OF_EMPLOYEES

URL = get_absolute_url("profile:edit-company-business-details")
EXPECTED_STRINGS = [
    "Business details",
    "Trading name",
    "Business URL",
    "How many employees are in your business?",
] + NO_OF_EMPLOYEES


def submit(
    actor: Actor,
    company: Company,
    *,
    title=True,
    website=True,
    size=True,
    sector=True,
    specific_title=None,
    specific_website=None,
    specific_size=None,
    specific_sector=None,
) -> (Response, Company):
    """Update basic Company's details: business name, website, keywords & size.

    Will use random details or specific values if they are provided.
    """
    session = actor.session

    if title:
        new_title = specific_title or f"{sentence()} AUTOTESTS"
    else:
        new_title = company.title

    if website:
        new_website = specific_website or (
            "https://{}.{}/".format(rare_word(), rare_word())
        )
    else:
        new_website = company.website

    if size:
        new_size = specific_size or random.choice(NO_OF_EMPLOYEES)
    else:
        new_size = company.no_employees

    if sector:
        random_sector, _ = random.choice(choices.INDUSTRIES)
        new_sector = specific_sector or random_sector
    else:
        new_sector = company.sector

    headers = {"Referer": URL}
    data = {
        "name": new_title,
        "website": new_website,
        "employees": new_size,
        "sectors": new_sector,
    }

    new_details = Company(
        title=new_title,
        website=new_website,
        sector=new_sector,
        no_employees=new_size,
    )

    response = make_request(
        Method.POST, URL, session=session, headers=headers, data=data
    )

    return response, new_details