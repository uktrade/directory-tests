# -*- coding: utf-8 -*-
"""Visit Britain Home Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import check_title, go_to_url, take_screenshot

NAME = "Home"
SERVICE = "Visit Britain"
TYPE = "home"
URL = urljoin(None, "")
PAGE_TITLE = "Visit Britain: The Official Tourism Website of Great Britain"
SELECTORS = {}


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_title(driver, PAGE_TITLE)
    logging.debug("All expected elements are visible on '%s' page", NAME)
