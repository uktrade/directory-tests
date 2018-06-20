# -*- coding: utf-8 -*-
"""Invest in Great Home Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import check_title, go_to_url
from utils import take_screenshot

NAME = "Invest in Great Home page"
URL = urljoin(None, "")
PAGE_TITLE = "Invest In Great Britain - Home"


def visit(driver: webdriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: webdriver):
    check_title(driver, PAGE_TITLE, exact_match=True)
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)
