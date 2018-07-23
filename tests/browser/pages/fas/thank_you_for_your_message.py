# -*- coding: utf-8 -*-
"""Find a Supplier - Thank you for your message Page Object."""
import logging
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
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
    "breadcrumbs": {"itself": Selector(By.CSS_SELECTOR, "p.breadcrumbs")},
    "message": {
        "itself": Selector(By.ID, "lede"),
        "header": Selector(By.CSS_SELECTOR, "#lede h2"),
        "go back link": Selector(By.CSS_SELECTOR, "#lede a"),
    },
}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_title(driver, PAGE_TITLE, exact_match=True)
    check_for_expected_sections_elements(driver, SELECTORS)
    logging.debug("All expected elements are visible on '%s' page", NAME)
