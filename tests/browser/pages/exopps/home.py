# -*- coding: utf-8 -*-
"""Export Opportunities Home Page Object."""
import logging

from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import common_selectors
from pages.common_actions import (
    check_url,
    find_and_click_on_page_element,
    go_to_url,
    take_screenshot,
)

NAME = "Home"
SERVICE = Service.EXPORT_OPPORTUNITIES
TYPE = PageType.HOME
URL = URLs.EXOPPS_LANDING.absolute
PAGE_TITLE = "Export opportunities"
SELECTORS = {}
SELECTORS.update(common_selectors.DOMESTIC_HEADER)
SELECTORS.update(common_selectors.DOMESTIC_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)
