# -*- coding: utf-8 -*-
"""Find a Supplier Empty Search Results Page Object."""
import logging
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    check_for_expected_sections_elements,
    check_for_section,
    check_title,
    check_url,
    take_screenshot,
)
from settings import DIRECTORY_UI_SUPPLIER_URL

NAME = "Empty Search Results"
SERVICE = "Find a Supplier"
TYPE = "search"
URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "search/")
PAGE_TITLE = "Search the database of UK suppliers' trade profiles - trade.great.gov.uk"

SELECTORS = {
    "filters": {
        "itself": Selector(By.ID, "ed-search-filters-container"),
        "title": Selector(By.ID, "ed-search-filters-title"),
        "filter list": Selector(By.ID, "id_sectors"),
    },
    "no results": {"itself": Selector(By.ID, "fassearch-no-results-content")},
}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    check_title(driver, PAGE_TITLE, exact_match=True)
    check_for_expected_sections_elements(driver, SELECTORS)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_section(driver: WebDriver, name: str):
    check_for_section(driver, SELECTORS, sought_section=name)
