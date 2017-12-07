# -*- coding: utf-8 -*-
"""Export Opportunities Home Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from settings import EXPORT_OPPORTUNITIES_UI_URL
from utils import assertion_msg, take_screenshot, wait_for_visibility

NAME = "Export Opportunities Home page"
URL = urljoin(EXPORT_OPPORTUNITIES_UI_URL, "")
PAGE_TITLE = "Exporting is GREAT"

WELCOME_MESSAGE = "#content-top > div.hero__specialContainer > h1"


def should_be_here(driver: webdriver):
    wait_for_visibility(driver, by_css=WELCOME_MESSAGE, time_to_wait=15)
    with assertion_msg(
            "Expected page title to be: '%s' but got '%s'", PAGE_TITLE,
            driver.title):
        assert driver.title.lower() == PAGE_TITLE.lower()
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)
