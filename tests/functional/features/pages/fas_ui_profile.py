# -*- coding: utf-8 -*-
"""FAB - Edit Company's Directory Profile page"""
import logging

from behave.model import Table
from requests import Response, Session

from tests import get_absolute_url
from tests.functional.features.context_utils import Company
from tests.functional.features.pages.common import DETAILS
from tests.functional.features.utils import (
    Method,
    assertion_msg,
    check_response,
    make_request
)
from tests.settings import SECTORS_WITH_LABELS

URL = get_absolute_url("ui-supplier:suppliers")
EXPECTED_STRINGS = [
    "Contact", "Facts &amp; details", "Company description",
    "Core industry", "Keywords", "Report profile", "Email company",
    "Contact company"
]


def go_to(session: Session, company_number: str) -> Response:
    """Go to "Edit Company's Details" page.

    This requires:
     * Supplier to be logged in

    :param session: Supplier session object
    :param company_number: (optional) explicit company number
    :return: response object
    """
    full_url = "{}/{}".format(URL, company_number)
    headers = {"Referer": get_absolute_url("ui-buyer:company-profile")}
    response = make_request(
        Method.GET, full_url, session=session, headers=headers)

    should_be_here(response, number=company_number)
    logging.debug(
        "Supplier is on the Company %s FAS profile page", company_number)
    return response


def should_be_here(response, *, number=None):
    """Check if User is on the correct page.

    :param response: response object
    """
    expected = EXPECTED_STRINGS + [number] if number else EXPECTED_STRINGS
    check_response(response, 200, body_contains=expected)
    logging.debug("Supplier is on FAS Company's Profile page")


def should_see_online_profiles(company: Company, response: Response):
    content = response.content.decode("utf-8")
    if company.facebook:
        with assertion_msg("Couldn't find link to company's Facebook profile"):
            assert "Visit Facebook" in content
            assert company.facebook in content
    if company.linkedin:
        with assertion_msg("Couldn't find link to company's LinkedIn profile"):
            assert "Visit LinkedIn" in content
            assert company.linkedin in content
    if company.twitter:
        with assertion_msg("Couldn't find link to company's Twitter profile"):
            assert "Visit Twitter" in content
            assert company.twitter in content


def should_not_see_online_profiles(response: Response):
    content = response.content.decode("utf-8")
    with assertion_msg("Found a link to 'Add Facebook' profile"):
        assert "Visit Facebook" not in content
    with assertion_msg("Found a link to 'Add LinkedIn' profile"):
        assert "Visit LinkedIn" not in content
    with assertion_msg("Found a link to 'Add Twitter' profile"):
        assert "Visit Twitter" not in content


def should_see_case_studies(case_studies: dict, response: Response):
    content = response.content.decode("utf-8")
    for case in case_studies:
        with assertion_msg(
                "Couldn't find Case Study '%s' title '%s'",
                case_studies[case].alias, case_studies[case].title):
            assert case_studies[case].title in content
        with assertion_msg(
                "Couldn't find Case Study '%s' description '%s'",
                case_studies[case].alias, case_studies[case].description):
            assert case_studies[case].description in content


def should_see_details(
        company: Company, response: Response, table_of_details: Table):
    """Supplier should see all expected Company details of FAS profile page.

    :param company: a namedtuple with Company details
    :param response: a response object
    :param table_of_details: a table of expected company details
    """
    visible_details = [row["detail"] for row in table_of_details]
    content = response.content.decode("utf-8")

    title = DETAILS["TITLE"] in visible_details
    keywords = DETAILS["KEYWORDS"] in visible_details
    website = DETAILS["WEBSITE"] in visible_details
    size = DETAILS["SIZE"] in visible_details
    sector = DETAILS["SECTOR"] in visible_details

    if title:
        with assertion_msg("Couldn't find Company's title '%s'", company.title):
            assert company.title in content
    if keywords:
        for keyword in company.keywords.split(", "):
            with assertion_msg("Couldn't find Company's keyword '%s'", keyword):
                assert keyword.strip() in content
    if website:
        with assertion_msg(
                "Couldn't find Company's website '%s'", company.website):
            assert company.website in content
    if size:
        with assertion_msg(
                "Couldn't find the size of the company '%s' in the response",
                company.no_employees):
            if company.no_employees == "10001+":
                assert "10,001+" in content
            elif company.no_employees == "1001-10000":
                assert "1,001-10,000" in content
            elif company.no_employees == "501-1000":
                assert "501-1,000" in content
            else:
                assert company.no_employees in content
    if sector:
        with assertion_msg(
                "Couldn't find company's sector '%s' in the response",
                SECTORS_WITH_LABELS[company.sector]):
            assert SECTORS_WITH_LABELS[company.sector] in content
