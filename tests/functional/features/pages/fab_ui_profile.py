# -*- coding: utf-8 -*-
"""FAB - Edit Company's Directory Profile page"""
import logging

from behave.model import Table
from requests import Response

from tests import get_absolute_url
from tests.functional.features.context_utils import Company
from tests.functional.features.pages.common import DETAILS
from tests.functional.features.utils import assertion_msg, check_response
from tests.settings import SECTORS_WITH_LABELS

URL = get_absolute_url("ui-buyer:company-profile")
EXPECTED_STRINGS = [
    "Facts &amp; details", "Number of employees", "Registration number",
    "Company description", "Online profiles", "Recent projects",
    "+ Add a case study", "Sectors of interest", "Keywords"
]

EXPECTED_STRINGS_NO_DESCRIPTION = [
    "Your company has no description.", "Set your description",
    "Your profile can't be published until your company has a description",
]

EXPECTED_STRINGS_VERIFIED = [
    "Your company is published", "View published profile",
    "Your profile is visible to international buyers"
]

EXPECTED_STRINGS_NOT_VERIFIED = [
    "Your company has not yet been verified.", "Verify your company",
    "Your profile can't be published until your company is verified"
]


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on FAB Company's Profile page")


def should_see_details(
        company: Company, response: Response, table_of_details: Table):
    """Supplier should see all expected Company details of FAB profile page.

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
        with assertion_msg(
                "Couldn't find company's title '%s' in the response",
                company.title):
            assert company.title in content
    if keywords:
        for keyword in company.keywords.split(", "):
            with assertion_msg(
                    "Couldn't find keyword '%s' in the response", keyword):
                assert keyword.strip() in content
    if website:
        with assertion_msg(
                "Couldn't find company's website '%s' in the response",
                company.website):
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
    logging.debug("Supplier can see all expected links to Online Profiles on "
                  "FAB Company's Directory Profile Page")


def should_not_see_online_profiles(response: Response):
    content = response.content.decode("utf-8")
    with assertion_msg("Found a link to 'Add Facebook' profile"):
        assert "Add Facebook" in content
    with assertion_msg("Found a link to 'Add LinkedIn' profile"):
        assert "Add LinkedIn" in content
    with assertion_msg("Found a link to 'Add Twitter' profile"):
        assert "Add Twitter" in content
    logging.debug("Supplier cannot see links to any Online Profile on FAB "
                  "Company's Directory Profile Page")


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
    logging.debug("Supplier can see all %d Case Studies on FAB Company's "
                  "Directory Profile Page", len(case_studies))


def should_see_profile_is_not_verified(response: Response):
    expected = EXPECTED_STRINGS + EXPECTED_STRINGS_NOT_VERIFIED
    check_response(response, 200, body_contains=expected)
    logging.debug("Supplier is on Unverified Company's Profile page")


def should_see_profile_is_verified(response: Response):
    expected = EXPECTED_STRINGS + EXPECTED_STRINGS_VERIFIED
    check_response(response, 200, body_contains=expected)
    logging.debug("Supplier is on Verified & Published Profile page")


def should_see_missing_description(response: Response):
    expected = EXPECTED_STRINGS + EXPECTED_STRINGS_NO_DESCRIPTION
    check_response(response, 200, body_contains=expected)
    logging.debug("Supplier is on FAB Profile page with missing description")
