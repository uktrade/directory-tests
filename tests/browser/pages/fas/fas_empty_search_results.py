# -*- coding: utf-8 -*-
"""Find a Supplier Empty Search Results Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import (
    check_for_expected_sections_elements,
    check_for_section,
    check_title,
    check_url,
    take_screenshot,
)
from settings import DIRECTORY_UI_SUPPLIER_URL

NAME = "Find a Empty Search Results page"
URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "search/")
PAGE_TITLE = (
    "Search the database of UK suppliers' trade profiles - trade.great.gov.uk"
)

SECTIONS = {
    "filters": {
        "itself": "#ed-search-filters-container",
        "title": "#ed-search-filters-title",
        "filter list": "#id_sectors",
    },
    "no results": {"itself": "#fassearch-no-results-content"},
}


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    check_title(driver, PAGE_TITLE, exact_match=True)
    check_for_expected_sections_elements(driver, SECTIONS)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_section(driver: webdriver, name: str):
    check_for_section(driver, SECTIONS, sought_section=name)
