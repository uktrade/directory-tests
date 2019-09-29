# -*- coding: utf-8 -*-
"""Profile - Enter your business details"""
import logging
import random

from requests import Response

from directory_tests_shared import BusinessType, PageType, Service, URLs
from directory_tests_shared.constants import POSTCODES, SECTORS
from tests.functional.utils.context_utils import Actor, Company
from tests.functional.utils.request import (
    Method,
    check_response,
    check_url,
    make_request,
)

SERVICE = Service.PROFILE
NAME = "Non Companies House company enter your business details"
TYPE = PageType.FORM
URL = URLs.PROFILE_ENROL_SOLE_TRADER_ENTER_BUSINESS_DETAILS.absolute
EXPECTED_STRINGS = [
    "I'm a sole trader or represent another type of UK business not registered with Companies House",
    "Enter your business details",
    "Business category",
    "Business name",
    "Business postcode",
    "I cannot find my business address",
    "Which industry is your business in?",
]

BUSINESS_CATEGORY = {
    BusinessType.SOLE_TRADER: "SOLE_TRADER",
    BusinessType.CHARITY: "CHARITY",
    BusinessType.PARTNERSHIP: "PARTNERSHIP",
    BusinessType.OTHER: "OTHER",
}


def should_be_here(response: Response):
    check_url(response, URL)
    check_response(response, 200, body_contains=EXPECTED_STRINGS)


def postcode_search(actor: Actor, postcode: str) -> dict:
    session = actor.session
    headers = {"Accept": "application/json"}
    url = URLs.PROFILE_API_POSTCODE_SEARCH.absolute_template.format(postcode=postcode)
    logging.debug(url)
    response = make_request(Method.GET, url, session=session, headers=headers)
    assert response.status_code == 200
    logging.debug(f"Found addresses for postcode: '{postcode}': {response.json()}")
    return random.choice(response.json())


def submit(actor: Actor, company: Company) -> Response:
    session = actor.session

    if (
        "address" in company.companies_house_details
        and "postal_code" in company.companies_house_details["address"]
    ):
        postcode = company.companies_house_details["address"]["postal_code"]
        address = postcode_search(actor, postcode)["value"]
    else:
        postcode = random.choice(POSTCODES)
        address = postcode_search(actor, postcode)["value"]

    headers = {"Referer": URL}
    files = {
        "csrfmiddlewaretoken": (None, actor.csrfmiddlewaretoken),
        "non_companies_house_enrolment_view-current_step": (None, "address-search"),
        "address-search-company_type": (None, BUSINESS_CATEGORY[company.business_type]),
        "address-search-company_name": (None, company.title),
        "address-search-postal_code": (None, postcode),
        "address-search-address": (None, address.replace(",", "\n")),
        "address-search-sectors": (None, random.choice(SECTORS)),
        "address-search-website": (None, "https://dit.automated.tests"),
    }

    # passing data as files will send it as "multipart/form-data" instead of default "application/x-www-form-urlencoded"
    return make_request(Method.POST, URL, session=session, headers=headers, files=files)
