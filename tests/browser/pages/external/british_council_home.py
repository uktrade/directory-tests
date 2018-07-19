# -*- coding: utf-8 -*-
"""British Council Home Page Object."""
import logging
from urllib.parse import urljoin

from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import check_title, go_to_url, take_screenshot

NAME = "Home"
SERVICE = "British Council"
TYPE = "home"
URL = urljoin(None, "")
PAGE_TITLE = "Study UK | British Council"
SELECTORS = {}


def visit(driver: WebDriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: WebDriver):
    check_title(driver, PAGE_TITLE, exact_match=True)
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)
