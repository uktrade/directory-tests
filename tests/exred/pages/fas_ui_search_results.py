# -*- coding: utf-8 -*-
"""Find a Supplier Search Results Page Object."""
import logging
from typing import List
from urllib.parse import urljoin

from selenium import webdriver
from utils import assertion_msg, find_elements, take_screenshot

from pages.common_actions import (
    check_for_expected_sections_elements,
    check_for_section,
    check_title,
    check_url,
)
from settings import DIRECTORY_UI_SUPPLIER_URL

NAME = "Find a Search results page"
URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "search/")
PAGE_TITLE = (
    "Search the database of UK suppliers' trade profiles - trade.great.gov.uk"
)

SECTOR_FILTERS = "#id_sectors input"
SECTIONS = {
    "filters": {
        "itself": "#ed-search-filters-container",
        "title": "#ed-search-filters-title",
        "filter list": "#id_sectors",
    },
    "results": {
        "itself": "#ed-search-list-container",
        "number of results": "#ed-search-list-container div.span8 > span",
        "pages top": "#ed-search-list-container > div:nth-child(1) span.current",
        "pages bottom": "div.company-profile-details-body-toolbar-bottom span.current",
    },
    "subscribe": {
        "itself": "div.ed-landing-page-form-container",
        "name": "#id_full_name",
        "email": "#id_email_address",
        "sector": "#id_sector",
        "company name": "#id_company_name",
        "country": "#id_country",
    },
}


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    check_title(driver, PAGE_TITLE, exact_match=True)
    check_for_expected_sections_elements(driver, SECTIONS)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_section(driver: webdriver, name: str):
    check_for_section(driver, SECTIONS, sought_section=name)


def should_see_filtered_results(
    driver: webdriver, expected_filters: List[str]
):
    def to_filter_format(name):
        return name.upper().replace(" ", "_").replace("-", "_")

    formatted_expected_filters = list(map(to_filter_format, expected_filters))

    sector_filters = find_elements(driver, by_css=SECTOR_FILTERS)
    checked_sector_filters = [
        sector_filter.get_attribute("value")
        for sector_filter in sector_filters
        if sector_filter.get_attribute("checked")
    ]

    number_expected_filters = len(formatted_expected_filters)
    number_checked_filters = len(checked_sector_filters)
    with assertion_msg(
        "Expected to see %d sector filter(s) to be checked but saw %d",
        number_expected_filters,
        number_checked_filters,
    ):
        assert number_checked_filters == number_expected_filters

    diff = list(set(formatted_expected_filters) - set(checked_sector_filters))
    with assertion_msg("Couldn't find '%s' among checked filters", diff):
        assert not diff
