# -*- coding: utf-8 -*-
"""Find a Supplier Home Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import check_title, check_url, go_to_url
from settings import DIRECTORY_UI_SUPPLIER_URL
from utils import take_screenshot

NAME = "Find a Supplier Home page"
URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "")
PAGE_TITLE = \
    "Find trade profiles of reliable UK suppliers - trade.great.gov.uk"


def visit(driver: webdriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: webdriver):
    check_url(driver, URL, exact_match=True)
    check_title(driver, PAGE_TITLE, exact_match=True)
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)
