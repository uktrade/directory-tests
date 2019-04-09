# -*- coding: utf-8 -*-
"""Find a Supplier Thank you for contacting supplier"""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    check_for_sections,
    go_to_url,
    take_screenshot,
)
from pages.fas.header_footer import HEADER_FOOTER_SELECTORS
from settings import DIRECTORY_UI_SUPPLIER_URL

NAME = "Thank you for contacting supplier"
SERVICE = "Find a Supplier"
TYPE = "contact"
URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "suppliers/{company_number}/contact/success/")
PAGE_TITLE = "Find a Buyer - GREAT.gov.uk"

SELECTORS = {
    "content": {
        "itself": Selector(By.ID, "content"),
        "heading": Selector(By.CSS_SELECTOR, "#content h1"),
        "description": Selector(By.CSS_SELECTOR, "#content p"),
        "browse more companies": Selector(
            By.CSS_SELECTOR, "#content div.ed-international-success-container a"
        ),
    }
}
SELECTORS.update(HEADER_FOOTER_SELECTORS)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    should_see_sections(driver, ["content"])
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)
