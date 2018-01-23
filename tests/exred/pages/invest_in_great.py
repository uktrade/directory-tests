# -*- coding: utf-8 -*-
"""Invest in Great Home Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import go_to_url
from utils import assertion_msg, take_screenshot

NAME = "Invest in Great Home page"
URL = urljoin(None, "")
PAGE_TITLE = "Invest home - invest.great.gov.uk"


def visit(driver: webdriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: webdriver):
    with assertion_msg(
            "Expected page title to be: '%s' but got '%s'", PAGE_TITLE,
            driver.title):
        assert driver.title.lower() == PAGE_TITLE.lower()
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)
