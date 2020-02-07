# -*- coding: utf-8 -*-
"""Find a Supplier - Company's Business Profile page"""
import logging
from urllib.parse import urljoin

from behave.model import Table
from requests import Response, Session
from scrapy import Selector

from directory_tests_shared import PageType, Service, URLs
from directory_tests_shared.constants import SECTORS_WITH_LABELS
from tests.functional.common import DETAILS
from tests.functional.utils.context_utils import Company
from tests.functional.utils.generic import (
    Method,
    assertion_msg,
    extract_page_contents,
    make_request,
)
from tests.functional.utils.request import check_response

SERVICE = Service.FAS
NAME = "Company's business profile"
TYPE = PageType.PROFILE
URL = URLs.FAS_SUPPLIER.absolute_template
EXPECTED_STRINGS = [
    "Business details",
    "Contact company",
    "Company description",
    "Core industry",
    "Report profile",
]


def go_to(session: Session, company_number: str) -> Response:
    """Go to Company's FAS profile page using company's number."""
    full_url = URL.format(ch_number=company_number)
    headers = {"Referer": URLs.PROFILE_BUSINESS_PROFILE.absolute}
    return make_request(Method.GET, full_url, session=session, headers=headers)


def go_to_endpoint(session: Session, endpoint: str) -> Response:
    """Go to Company's FAS profile page using explicit FAS endpoint.

    :param endpoint: FAS endpoint that leads directly to Company's profile page
    """
    fas_url = URLs.FAS_LANDING.absolute
    profile_url = urljoin(fas_url, endpoint)
    return make_request(Method.GET, profile_url, session=session)


def should_be_here(response, *, number=None):
    expected = EXPECTED_STRINGS + [number] if number else EXPECTED_STRINGS
    check_response(response, 200, body_contains=expected)
    logging.debug("Supplier is on FAS Company's Profile page")


def should_see_online_profiles(company: Company, response: Response):
    content = response.content.decode("utf-8")
    if company.facebook:
        with assertion_msg("Couldn't find link to company's Facebook profile"):
            assert "Visit company Facebook" in content
            assert company.facebook in content
    if company.linkedin:
        with assertion_msg("Couldn't find link to company's LinkedIn profile"):
            assert "Visit company LinkedIn" in content
            assert company.linkedin in content
    if company.twitter:
        with assertion_msg("Couldn't find link to company's Twitter profile"):
            assert "Visit company Twitter" in content
            assert company.twitter in content


def should_not_see_online_profiles(response: Response):
    content = response.content.decode("utf-8").lower()
    with assertion_msg("Found a link to 'visit Facebook' profile"):
        assert "visit company facebook" not in content
    with assertion_msg("Found a link to 'visit LinkedIn' profile"):
        assert "visit company linkedin" not in content
    with assertion_msg("Found a link to 'visit Twitter' profile"):
        assert "visit company twitter" not in content


def should_see_case_studies(case_studies: dict, response: Response):
    content = response.content.decode("utf-8")
    for case in case_studies:
        with assertion_msg(
            "Couldn't find Case Study '%s' title '%s'",
            case_studies[case].alias,
            case_studies[case].title,
        ):
            assert case_studies[case].title in content
        with assertion_msg(
            "Couldn't find Case Study '%s' description '%s'",
            case_studies[case].alias,
            case_studies[case].description,
        ):
            assert case_studies[case].summary in content


def should_see_details(company: Company, response: Response, table_of_details: Table):
    """Supplier should see all expected Company details of FAS profile page.

    :param company: a namedtuple with Company details
    :param response: a response object
    :param table_of_details: a table of expected company details
    """
    visible_details = [row["detail"] for row in table_of_details]
    content = extract_page_contents(response.content.decode("utf-8")).lower()

    title = DETAILS["NAME"] in visible_details
    keywords = DETAILS["KEYWORDS"] in visible_details
    website = DETAILS["WEBSITE"] in visible_details
    size = DETAILS["SIZE"] in visible_details
    sector = DETAILS["SECTOR"] in visible_details

    if title:
        with assertion_msg("Couldn't find Company's title '%s'", company.title):
            assert company.title.lower() in content
        logging.debug(f"Found title: '{company.title}' on: {response.url}")
    if keywords:
        for keyword in company.keywords.split(", "):
            with assertion_msg("Couldn't find Company's keyword '%s'", keyword):
                assert keyword.strip().lower() in content
        logging.debug(f"Found keywords: '{company.keywords}' on: {response.url}")
    if website:
        with assertion_msg("Couldn't find Company's website '%s'", company.website):
            assert company.website.lower() in content
        logging.debug(f"Found website: '{company.website}' on: {response.url}")
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
        logging.debug(f"Found size: '{company.no_employees}' on: {response.url}")
    if sector:
        with assertion_msg(
            "Couldn't find company's sector '%s' in the response",
            SECTORS_WITH_LABELS[company.sector],
        ):
            assert SECTORS_WITH_LABELS[company.sector].lower() in content
        logging.debug(f"Found sector: '{company.sector}' on: {response.url}")
    logging.debug(f"Found all expected details on: {response.url}")


def get_case_studies_details(response: Response):
    content = response.content.decode("utf-8")
    article_selector = "div.card"
    articles = Selector(text=content).css(article_selector).extract()
    result = []
    for article in articles:
        title = Selector(text=article).css("h3::text").extract()[0]
        summary = Selector(text=article).css("p.description::text").extract()[0]
        href = Selector(text=article).css("a::attr(href)").extract()[0]
        slug = href.split("/")[-2]
        assert slug, f"Couldn't extract case study slug from {article}"
        logging.debug("Got case study slug: %s", slug)
        result.append((title, summary, href, slug))
    assert result, f"No Case Study details extracted from {articles}"
    return result
