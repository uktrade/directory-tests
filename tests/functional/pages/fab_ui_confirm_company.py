# -*- coding: utf-8 -*-
"""FAB - Confirm Company page"""
import logging
from urllib.parse import urljoin

from requests import Response, Session
from tests import get_absolute_url
from tests.functional.utils.context_utils import Company
from tests.functional.utils.generic import escape_html
from tests.functional.utils.request import Method, check_response, make_request

URL = get_absolute_url('ui-buyer:landing')
EXPECTED_STRINGS = [
    "Create your business profile", "Confirm company", "Trading status",
    "Company number", "Registered address",
    ("I confirm that I am authorised to sign this company up to great.gov.uk "
     "services"), "Creating an account means you can",
    ("create a free business profile to promote your products and services to "
     "overseas buyers"),
    ("apply for opportunities sourced by overseas trade professionals or "
     "provided by a third party"), "Register"
]


def go_to(session: Session, company: Company) -> Response:
    data = {"company_name": company.title, "company_number": company.number}
    headers = {"Referer": URL}

    response = make_request(
        Method.POST, URL, session=session, headers=headers, data=data)

    return response


def should_be_here(response: Response, company: Company):
    escaped_company_title = escape_html(company.title, upper=True)
    expected = EXPECTED_STRINGS + [escaped_company_title, company.number]
    check_response(response, 200, body_contains=expected)
    logging.debug("Successfully got to the Confirm your Company page")


def confirm_company_selection(
        session: Session, company: Company, token: str) -> Response:
    query = "?company_number={}".format(company.number)
    url = urljoin(get_absolute_url('ui-buyer:register-confirm-company'), query)
    headers = {"Referer": url}
    data = {
        "csrfmiddlewaretoken": token,
        "enrolment_view-current_step": "company",
        "company-company_name": company.title,
        "company-company_number": company.number,
        "company-company_address":
            company.companies_house_details["address_snippet"]
    }

    return make_request(
        Method.POST, url, session=session, headers=headers, data=data)
