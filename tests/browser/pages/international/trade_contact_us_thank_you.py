# -*- coding: utf-8 -*-
"""Find a Supplier - Thank you for your message."""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import Services, common_selectors
from pages.common_actions import (
    Selector,
    check_for_sections,
    check_url,
    go_to_url,
    take_screenshot,
)
from settings import DIRECTORY_UI_SUPPLIER_URL

NAME = "Find a UK business partner"
SERVICE = Services.INTERNATIONAL
TYPE = "Thank you for your message"
URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "contact/success/")
PAGE_TITLE = "Find a Buyer - GREAT.gov.uk"

SELECTORS = {
    "content": {
        "itself": Selector(By.ID, "content"),
        "heading": Selector(By.CSS_SELECTOR, "#content h2"),
        "description": Selector(By.CSS_SELECTOR, "#content p"),
    }
}
SELECTORS.update(common_selectors.INTERNATIONAL_HEADER_WO_LANGUAGE_SELECTOR)
SELECTORS.update(common_selectors.INTERNATIONAL_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver, *, company_number: str = None):
    if company_number:
        url = URL.format(company_number=company_number)
    else:
        url = URL.format(company_number="07399608")
    check_url(driver, url, exact_match=False)
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)
