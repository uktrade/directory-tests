# -*- coding: utf-8 -*-
"""FAB - Edit Company's Directory Profile page"""
import logging

from tests import get_absolute_url
from tests.functional.features.pages.common import DETAILS
from tests.functional.features.utils import check_response
from tests.settings import SECTORS_WITH_LABELS

URL = get_absolute_url("ui-buyer:company-profile")
EXPECTED_STRINGS = [
    "Facts &amp; details", "Number of employees", "Registration number",
    "Company description", "Online profiles", "Recent projects",
    "+ Add a case study", "Sectors of interest", "Keywords"
]


def should_be_here(response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on FAB Company's Profile page")


def should_see_details(context, supplier_alias, table_of_details):
    visible_details = [row["detail"] for row in table_of_details]
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    content = context.response.content.decode("utf-8")

    title = DETAILS["TITLE"] in visible_details
    keywords = DETAILS["KEYWORDS"] in visible_details
    website = DETAILS["WEBSITE"] in visible_details
    size = DETAILS["SIZE"] in visible_details
    sector = DETAILS["SECTOR"] in visible_details

    if title:
        assert company.title in content
    if keywords:
        for keyword in company.keywords.split(", "):
            assert keyword.strip() in content
    if website:
        assert company.website in content
    if size:
        if company.no_employees == "10001+":
            assert "10,001+" in content
        elif company.no_employees == "1001-10000":
            assert "1,001-10,000" in content
        elif company.no_employees == "501-1000":
            assert "501-1,000" in content
        else:
            assert company.no_employees in content
    if sector:
        assert SECTORS_WITH_LABELS[company.sector] in content
    logging.debug("% can see all expected details are visible of FAB Company's "
                  "Directory Profile Page", supplier_alias)
