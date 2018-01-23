# -*- coding: utf-8 -*-
"""Export Opportunities Home Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import check_title, check_url, go_to_url
from settings import EXPORT_OPPORTUNITIES_UI_URL
from utils import take_screenshot, wait_for_visibility

NAME = "Export Opportunities Home page"
URL = urljoin(EXPORT_OPPORTUNITIES_UI_URL, "")
PAGE_TITLE = "Export opportunities"

WELCOME_MESSAGE = "#content-top > div.hero__specialContainer > h1"


def visit(driver: webdriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: webdriver):
    wait_for_visibility(driver, by_css=WELCOME_MESSAGE, time_to_wait=15)
    check_url(driver, URL, exact_match=True)
    check_title(driver, PAGE_TITLE, exact_match=True)
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)
