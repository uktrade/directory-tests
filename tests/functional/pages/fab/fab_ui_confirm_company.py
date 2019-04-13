# -*- coding: utf-8 -*-
"""FAB - Confirm Company page"""
import logging
from urllib.parse import urljoin

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.pages import Services
from tests.functional.utils.context_utils import Company
from tests.functional.utils.generic import escape_html
from tests.functional.utils.request import (
    Method,
    check_response,
    check_url,
    make_request,
)

SERVICE = Services.FAB
NAME = "Confirm company"
TYPE = "form"
URL = get_absolute_url("ui-buyer:landing")
POST_URL = get_absolute_url("ui-buyer:register-confirm-company")
EXPECTED_STRINGS = [
    "Confirm your company",
    "Registered name",
    "Company number",
    "Registered address",
    "I confirm that I am authorised to sign this company up to great.gov.uk",
]


def go_to(session: Session, company: Company) -> Response:
    data = {"company_name": company.title, "company_number": company.number}
    headers = {"Referer": URL}
    return make_request(
        Method.POST, URL, session=session, headers=headers, data=data
    )


def should_be_here(response: Response, company: Company):
    expected_url = f"{POST_URL}?company_number={company.number}"
    check_url(response, expected_url)
    escaped_company_title = escape_html(company.title, upper=True)
    expected = EXPECTED_STRINGS + [escaped_company_title, company.number]
    check_response(response, 200, body_contains=expected)
    logging.debug("Successfully got to the Confirm your Company page")


def confirm_company_selection(
    session: Session, company: Company, token: str
) -> Response:
    query = "?company_number={}".format(company.number)
    url = urljoin(get_absolute_url("ui-buyer:register-confirm-company"), query)
    headers = {"Referer": url}
    data = {
        "csrfmiddlewaretoken": token,
        "enrolment_view-current_step": "company",
        "company-company_name": company.title,
        "company-company_number": company.number,
        "company-confirmed": "on",
        "company-company_address": company.companies_house_details[
            "address_snippet"
        ],
    }

    return make_request(
        Method.POST, url, session=session, headers=headers, data=data
    )
