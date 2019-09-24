# -*- coding: utf-8 -*-
"""Visit Britain Home Page Object."""
import logging

from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared.enums import Service
from pages.common_actions import check_url, take_screenshot

NAME = "Home"
SERVICE = Service.VISIT_BRITAIN
TYPE = "home"
URL = "https://www.visitbritain.com/"
SELECTORS = {}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)
