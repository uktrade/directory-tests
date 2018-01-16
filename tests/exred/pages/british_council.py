# -*- coding: utf-8 -*-
"""British Council Home Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import visit as common_visit
from utils import assertion_msg, take_screenshot

NAME = "British Council Home page"
URL = urljoin(None, "")
PAGE_TITLE = "Study UK | British Council"


def visit(driver: webdriver, *, first_time: bool = False):
    common_visit(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: webdriver):
    with assertion_msg(
            "Expected page title to be: '%s' but got '%s'", PAGE_TITLE,
            driver.title):
        assert driver.title.lower() == PAGE_TITLE.lower()
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)
