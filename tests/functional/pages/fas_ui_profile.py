# -*- coding: utf-8 -*-
"""FAB - Edit Company's Directory Profile page"""
import logging
from urllib.parse import urljoin

from behave.model import Table
from requests import Response, Session
from tests import get_absolute_url
from tests.functional.common import DETAILS
from tests.functional.utils.context_utils import Company
from tests.functional.utils.generic import Method, assertion_msg, make_request
from tests.functional.utils.request import check_response
from tests.settings import SECTORS_WITH_LABELS

from scrapy import Selector

URL = get_absolute_url("ui-supplier:suppliers")
EXPECTED_STRINGS = [
    "Contact", "Facts &amp; details", "Company description",
    "Core industry", "Keywords", "Report profile", "Email company",
    "Contact company"
]


def go_to(session: Session, company_number: str) -> Response:
    """Go to Company's FAS profile page using company's number.

    :param session: Supplier session object
    :param company_number: (optional) explicit company number
    :return: response object
    """
    full_url = urljoin(URL, company_number)
    headers = {"Referer": get_absolute_url("ui-buyer:company-profile")}
    response = make_request(
        Method.GET, full_url, session=session, headers=headers)

    should_be_here(response, number=company_number)
    logging.debug(
        "User is on the Company %s FAS profile page", company_number)
    return response


def go_to_endpoint(session: Session, endpoint: str) -> Response:
    """Go to Company's FAS profile page using explicit FAS endpoint.

    :param session: Supplier session object
    :param endpoint: FAS endpoint that leads directly to Company's profile page
    :return: response object
    """
    fas_url = get_absolute_url("ui-supplier:landing")
    profile_url = urljoin(fas_url, endpoint)
    return make_request(Method.GET, profile_url, session=session)


def should_be_here(response, *, number=None):
    """Check if User is on the correct page.

    :param response: response object
    :param number: (optional) expected company number
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
            assert case_studies[case].summary in content


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


def get_case_studies_details(response: Response):
    content = response.content.decode("utf-8")
    article_selector = "#company-projects > article"
    articles = Selector(text=content).css(article_selector).extract()
    result = []
    for article in articles:
        title = Selector(text=article).css("h3::text").extract()[0]
        summary = Selector(text=article).css("p::text").extract()[0]
        href = Selector(text=article).css("a::attr(href)").extract()[0]
        slug = href.split("/")[-2]
        assert slug, "Could not extract case study slug from {}".format(article)
        logging.debug("Got case study slug: %s", slug)
        result.append((title, summary, href, slug))
    assert result, "No Case Study details extracted from {}".format(articles)
    return result
