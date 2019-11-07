# -*- coding: utf-8 -*-
"""Contact Us - Feedback Page Object."""
import logging

from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages.common_actions import check_url, go_to_url, take_screenshot

NAME = "Feedback"
SERVICE = Service.INVEST
TYPE = PageType.CONTACT_US
URL = URLs.CONTACT_US_FEEDBACK.absolute
PAGE_TITLE = "Contact us - great.gov.uk"
SELECTORS = {}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, PAGE_TITLE)
    check_url(driver, URL, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)
