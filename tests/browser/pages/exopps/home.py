# -*- coding: utf-8 -*-
"""Export Opportunities Home Page Object."""
import logging
from urllib.parse import urljoin

from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    check_url,
    go_to_url,
    take_screenshot,
)
from settings import EXPORT_OPPORTUNITIES_UI_URL

NAME = "Home"
SERVICE = "Export Opportunities"
TYPE = "home"
URL = urljoin(EXPORT_OPPORTUNITIES_UI_URL, "")
PAGE_TITLE = "Export opportunities"
SELECTORS = {}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", NAME)
