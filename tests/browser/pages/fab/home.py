# -*- coding: utf-8 -*-
"""Find a Buyer Home Page Object."""
import logging
from urllib.parse import urljoin

from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import check_title, check_url, go_to_url, take_screenshot
from settings import DIRECTORY_UI_BUYER_URL

NAME = "Home"
SERVICE = "Find a Buyer"
TYPE = "home"
URL = urljoin(DIRECTORY_UI_BUYER_URL, "")
PAGE_TITLE = "Business profile - great.gov.uk"

SELECTORS = {}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", NAME)
