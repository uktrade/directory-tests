# -*- coding: utf-8 -*-
"""Export Opportunities Home Page Object."""
import logging
from urllib.parse import urljoin

from selenium.webdriver.remote.webdriver import WebDriver

from pages import Services, common_selectors
from pages.common_actions import (
    check_url,
    find_and_click_on_page_element,
    go_to_url,
    take_screenshot,
)
from directory_tests_shared.settings import EXPORT_OPPORTUNITIES_URL

NAME = "Home"
SERVICE = Services.EXPORT_OPPORTUNITIES
TYPE = "home"
URL = urljoin(EXPORT_OPPORTUNITIES_URL, "")
PAGE_TITLE = "Export opportunities"
SELECTORS = {}
SELECTORS.update(common_selectors.HEADER)
SELECTORS.update(common_selectors.FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)
