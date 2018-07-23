# -*- coding: utf-8 -*-
"""External site - Legal Services Page Object."""
import logging

from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import check_url, take_screenshot

NAME = "Home"
SERVICE = "Legal Services"
TYPE = "home"
URL = "https://medium.com/legal-services-are-great"
SELECTORS = {}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, SERVICE)
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)
