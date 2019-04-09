# -*- coding: utf-8 -*-
"""Find a Supplier Search Results Page Object."""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    assertion_msg,
    check_for_sections,
    check_url,
    find_elements,
    take_screenshot,
)
from pages.fas.header_footer import HEADER_FOOTER_SELECTORS
from settings import DIRECTORY_UI_SUPPLIER_URL

NAME = "Search results"
SERVICE = "Find a Supplier"
TYPE = "search"
URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "search/")
PAGE_TITLE = "Search the database of UK suppliers' trade profiles - trade.great.gov.uk"

SECTOR_FILTERS = Selector(By.CSS_SELECTOR, "#id_sectors input")
SELECTORS = {
    "filters": {
        "itself": Selector(By.ID, "ed-search-filters-container"),
        "title": Selector(By.ID, "ed-search-filters-title"),
        "filter list": Selector(By.ID, "id_sectors"),
    },
    "results": {
        "itself": Selector(By.ID, "ed-search-list-container"),
        "number of results": Selector(
            By.CSS_SELECTOR, "#ed-search-list-container div.span8 > span"
        ),
        "pages top": Selector(
            By.CSS_SELECTOR, "#ed-search-list-container > div:nth-child(1) span.current"
        ),
        "pages bottom": Selector(
            By.CSS_SELECTOR,
            "div.company-profile-details-body-toolbar-bottom span.current",
        ),
    },
    "subscribe": {
        "itself": Selector(By.CSS_SELECTOR, "div.ed-landing-page-form-container"),
        "name": Selector(By.ID, "id_full_name"),
        "email": Selector(By.ID, "id_email_address"),
        "sector": Selector(By.ID, "id_sector"),
        "company name": Selector(By.ID, "id_company_name"),
        "country": Selector(By.ID, "id_country"),
    },
}
SELECTORS.update(HEADER_FOOTER_SELECTORS)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def should_see_filtered_results(driver: WebDriver, expected_filters: List[str]):
    def to_filter_format(name):
        return name.upper().replace(" ", "_").replace("-", "_")

    formatted_expected_filters = list(map(to_filter_format, expected_filters))

    sector_filters = find_elements(driver, SECTOR_FILTERS)
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
