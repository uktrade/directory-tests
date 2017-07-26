# -*- coding: utf-8 -*-
"""FAB - Edit Company's Directory Profile page"""
import logging

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.features.context_utils import Company
from tests.functional.features.utils import Method, check_response, make_request

URL = get_absolute_url("ui-supplier:suppliers")
EXPECTED_STRINGS = [
    "Contact",
    "Company description",
    "Facts &amp; details",
    "Industries of interest",
    "Keywords",
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
    expected = EXPECTED_STRINGS + [number] if number else EXPECTED_STRINGS
    check_response(response, 200, body_contains=expected)
    logging.debug("Supplier is on FAS Company's Profile page")


def should_see_online_profiles(company: Company, response: Response):
    content = response.content.decode("utf-8")
    if company.facebook:
        assert "Visit Facebook" in content
        assert company.facebook in content
    if company.linkedin:
        assert "Visit LinkedIn" in content
        assert company.linkedin in content
    if company.twitter:
        assert "Visit Twitter" in content
        assert company.twitter in content


def should_not_see_online_profiles(response: Response):
    content = response.content.decode("utf-8")
    assert "Visit Facebook" not in content
    assert "Visit LinkedIn" not in content
    assert "Visit Twitter" not in content


def should_see_case_studies(case_studies: dict, response: Response):
    content = response.content.decode("utf-8")
    for case in case_studies:
        assert case_studies[case].title in content
        assert case_studies[case].description in content
