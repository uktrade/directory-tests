# -*- coding: utf-8 -*-
"""Find a Supplier Thank you for contacting supplier"""
import logging
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import common_selectors
from pages.common_actions import Selector, check_for_sections

NAME = "Thank you for contacting supplier"
SERVICE = Service.FAS
TYPE = PageType.CONTACT_US
URL = URLs.FAS_CONTACT_SUPPLIER_SUCCESS.absolute_template
PAGE_TITLE = "Find a Buyer - GREAT.gov.uk"

SELECTORS = {
    "content": {
        "itself": Selector(By.CSS_SELECTOR, "div.message-box-with-icon"),
        "heading": Selector(By.CSS_SELECTOR, "div.message-box-with-icon h3"),
        "description": Selector(By.CSS_SELECTOR, "div.message-box-with-icon p"),
        "browse more companies": Selector(By.CSS_SELECTOR, "#next-container a"),
    }
}
SELECTORS.update(common_selectors.INTERNATIONAL_HEADER_WO_LANGUAGE_SELECTOR)
SELECTORS.update(common_selectors.INTERNATIONAL_FOOTER)


def should_be_here(driver: WebDriver):
    should_see_sections(driver, ["content"])
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)
