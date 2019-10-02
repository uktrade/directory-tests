# -*- coding: utf-8 -*-
"""Profile - Edit Company's Business Profile page"""
import logging

from behave.model import Table
from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from directory_tests_shared.constants import SECTORS_WITH_LABELS
from tests.functional.common import DETAILS
from tests.functional.utils.context_utils import Company
from tests.functional.utils.generic import assertion_msg, escape_html
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Service.PROFILE
NAME = "Edit company profile"
TYPE = PageType.LANDING
URL = URLs.PROFILE_BUSINESS_PROFILE.absolute
EXPECTED_STRINGS = [
    "You are signed in as",
    "Business profile",
    "Personal details",
    "Profile email",
]

EXPECTED_STRINGS_NO_DESCRIPTION = ["Add a business description"]

EXPECTED_STRINGS_VERIFIED = [
    "Publish your business profile",
    "You can now publish your business profile",
]

EXPECTED_STRINGS_PUBLISHED = ["View Find a Supplier profile"]

EXPECTED_STRINGS_NOT_VERIFIED = [
    "Confirm your identity",
    "For security reasons, we need to check you're who you say you are",
]
EXPECTED_STRINGS_REQUEST_VERIFICATION = [
    "Your business profile is ready to be verified",
    "Profile ready to be verified",
    "Request to verify",
]


def go_to(session: Session) -> Response:
    headers = {"Referer": URL}
    return make_request(Method.GET, URL, session=session, headers=headers)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on Profile - Edit Company's Profile page")


def should_see_details(company: Company, response: Response, table_of_details: Table):
    """Supplier should see all expected Company details of Profile page."""
    visible_details = [row["detail"] for row in table_of_details]
    content = response.content.decode("utf-8")

    title = DETAILS["NAME"] in visible_details
    keywords = DETAILS["KEYWORDS"] in visible_details
    website = DETAILS["WEBSITE"] in visible_details
    size = DETAILS["SIZE"] in visible_details
    sector = DETAILS["SECTOR"] in visible_details

    if title:
        with assertion_msg(
            "Couldn't find company's title '%s' in the response", company.title
        ):
            assert company.title in content
    if keywords:
        for keyword in company.keywords.split(", "):
            with assertion_msg("Couldn't find keyword '%s' in the response", keyword):
                assert escape_html(keyword.strip()) in content
    if website:
        with assertion_msg(
            "Couldn't find company's website '%s' in the response", company.website
        ):
            assert company.website in content
    if size:
        with assertion_msg(
            "Couldn't find the size of the company '%s' in the response",
            company.no_employees,
        ):
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
            SECTORS_WITH_LABELS[company.sector],
        ):
            assert SECTORS_WITH_LABELS[company.sector].lower() in content.lower()


def should_see_online_profiles(company: Company, response: Response):
    content = response.content.decode("utf-8")

    if company.facebook:
        with assertion_msg("Couldn't find link to company's Facebook profile"):
            assert company.facebook in content
    if company.linkedin:
        with assertion_msg("Couldn't find link to company's LinkedIn profile"):
            assert company.linkedin in content
    if company.twitter:
        with assertion_msg("Couldn't find link to company's Twitter profile"):
            assert company.twitter in content
    logging.debug(
        "Supplier can see all expected links to Online Profiles on "
        "FAB Company's Directory Profile Page"
    )


def should_not_see_links_to_online_profiles(response: Response):
    content = response.content.decode("utf-8").lower()
    with assertion_msg("Found a link to Facebook profile"):
        assert "add facebook" in content
    with assertion_msg("Found a link to LinkedIn profile"):
        assert "add linkedin" in content
    with assertion_msg("Found a link to Twitter profile"):
        assert "add twitter" in content
    logging.debug(
        "Supplier cannot see links to any Online Profile on FAB "
        "Company's Directory Profile Page"
    )


def should_see_case_studies(case_studies: dict, response: Response):
    content = response.content.decode("utf-8")
    for case in case_studies:
        with assertion_msg(
            "Couldn't find Case Study '%s' title '%s'",
            case_studies[case].alias,
            case_studies[case].title,
        ):
            assert case_studies[case].title in content
    logging.debug(
        "Supplier can see all %d Case Studies on FAB Company's "
        "Directory Profile Page",
        len(case_studies),
    )


def should_see_profile_is_not_verified(response: Response, *, ch_company: bool = True):
    if ch_company:
        expected = EXPECTED_STRINGS + EXPECTED_STRINGS_NOT_VERIFIED
    else:
        expected = EXPECTED_STRINGS + EXPECTED_STRINGS_REQUEST_VERIFICATION
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


def should_see_profile_is_published(response: Response):
    expected = EXPECTED_STRINGS + EXPECTED_STRINGS_PUBLISHED
    check_response(response, 200, body_contains=expected)
    logging.debug("Supplier is on Published Profile page")
