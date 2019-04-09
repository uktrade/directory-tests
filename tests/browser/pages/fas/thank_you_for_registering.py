# -*- coding: utf-8 -*-
"""Find a Supplier - Thank you for registering to an email subscription."""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    check_for_sections,
    check_url,
    go_to_url,
    take_screenshot,
)
from pages.fas.header_footer import HEADER_FOOTER_SELECTORS
from settings import DIRECTORY_UI_SUPPLIER_URL

NAME = "Thank you for registering"
SERVICE = "Find a Supplier"
TYPE = "contact"
URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "subscribe/")
PAGE_TITLE = "Find a Buyer - GREAT.gov.uk"

SELECTORS = {
    "message": {
        "itself": Selector(By.ID, "content"),
        "heading": Selector(By.CSS_SELECTOR, "#content h1"),
        "description": Selector(By.CSS_SELECTOR, "#content p"),
    }
}
SELECTORS.update(HEADER_FOOTER_SELECTORS)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=True)
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)
