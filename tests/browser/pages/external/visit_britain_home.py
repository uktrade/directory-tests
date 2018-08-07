# -*- coding: utf-8 -*-
"""Visit Britain Home Page Object."""
import logging
from urllib.parse import urljoin

from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import check_title, take_screenshot

NAME = "Home"
SERVICE = "Visit Britain"
TYPE = "home"
URL = urljoin(None, "")
PAGE_TITLE = "VisitBritain | VisitBritain"
SELECTORS = {}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_title(driver, PAGE_TITLE)
    logging.debug("All expected elements are visible on '%s' page", NAME)
