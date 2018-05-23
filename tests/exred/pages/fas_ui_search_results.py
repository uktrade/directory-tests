# -*- coding: utf-8 -*-
"""Find a Supplier Search Results Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import (
    check_for_expected_sections_elements,
    check_for_section,
    check_title,
    check_url,
)
from settings import DIRECTORY_UI_SUPPLIER_URL
from utils import take_screenshot

NAME = "Find a Search results page"
URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "search/")
PAGE_TITLE = \
    "Search the database of UK suppliers' trade profiles - trade.great.gov.uk"

SECTIONS = {
    "filters": {
        "itself": "#ed-search-filters-container",
        "title": "#ed-search-filters-title",
        "filter list": "#id_sectors"
    },
    "results": {
        "itself": "#ed-search-list-container",
        "number of results": "#ed-search-list-container div.span8 > span",
        "pages top": "#ed-search-list-container > div:nth-child(1) span.current",
        "pages bottom": "div.company-profile-details-body-toolbar-bottom span.current"
    },
    "subscribe": {
        "itself": "div.ed-landing-page-form-container",
        "name": "#id_full_name",
        "email": "#id_email_address",
        "sector": "#id_sector",
        "company name": "#id_company_name",
        "country": "#id_country",
    }
}


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    check_title(driver, PAGE_TITLE, exact_match=True)
    check_for_expected_sections_elements(driver, SECTIONS)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_section(driver: webdriver, name: str):
    check_for_section(driver, SECTIONS, sought_section=name)
