# -*- coding: utf-8 -*-
"""Visit Britain Home Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import check_title, go_to_url
from utils import take_screenshot

NAME = "Visit Britain Home page"
URL = urljoin(None, "")
PAGE_TITLE = "Visit Britain: The Official Tourism Website of Great Britain"


def visit(driver: webdriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_title(driver, PAGE_TITLE)
    logging.debug("All expected elements are visible on '%s' page", NAME)
