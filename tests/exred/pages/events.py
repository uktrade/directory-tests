# -*- coding: utf-8 -*-
"""Events Home Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from settings import EVENTS_UI_URL
from utils import assertion_msg, take_screenshot, wait_for_visibility

NAME = "Events Home page"
URL = urljoin(EVENTS_UI_URL, "")
PAGE_TITLE = "Department for International Trade (DIT): exporting from or investing in the UK"

WELCOME_MESSAGE = "#feature > div.contain.slider > article.tile.initial.visible > div > h2"


def should_be_here(driver: webdriver):
    wait_for_visibility(driver, by_css=WELCOME_MESSAGE, time_to_wait=15)
    with assertion_msg(
            "Expected page title to be: '%s' but got '%s'", PAGE_TITLE,
            driver.title):
        assert driver.title.lower() == PAGE_TITLE.lower()
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)
