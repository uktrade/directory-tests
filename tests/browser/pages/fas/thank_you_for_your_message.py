# -*- coding: utf-8 -*-
"""Find a Supplier - Thank you for your message Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import (
    check_for_expected_sections_elements,
    check_title,
    take_screenshot,
)
from settings import DIRECTORY_UI_SUPPLIER_URL

NAME = "Thank you for your message"
SERVICE = "Find a Supplier"
TYPE = "contact"
URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "industries/contact/")
PAGE_TITLE = "Contact us - trade.great.gov.uk"

SELECTORS = {
    "breadcrumbs": {"itself": "p.breadcrumbs"},
    "message": {
        "itself": "#lede",
        "header": "#lede > div > h2",
        "go back link": "#lede a",
    },
}


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_title(driver, PAGE_TITLE, exact_match=True)
    check_for_expected_sections_elements(driver, SELECTORS)
    logging.debug("All expected elements are visible on '%s' page", NAME)
