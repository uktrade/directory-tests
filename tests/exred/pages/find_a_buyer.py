# -*- coding: utf-8 -*-
"""Find a Buyer Home Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import visit as common_visit
from settings import DIRECTORY_UI_BUYER_URL
from utils import assertion_msg, take_screenshot

NAME = "Find a Buyer Home page"
URL = urljoin(DIRECTORY_UI_BUYER_URL, "")
PAGE_TITLE = "Find a Buyer - GREAT.gov.uk"


def visit(driver: webdriver, *, first_time: bool = False):
    common_visit(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: webdriver):
    with assertion_msg(
            "Expected page title to be: '%s' but got '%s'", PAGE_TITLE,
            driver.title):
        assert driver.title.lower() == PAGE_TITLE.lower()
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)
