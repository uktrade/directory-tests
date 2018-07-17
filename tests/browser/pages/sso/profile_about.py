# -*- coding: utf-8 -*-
"""SSO Confirm Your Email Address Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import (
    check_for_expected_elements,
    check_title,
    check_url,
    go_to_url,
    take_screenshot,
)
from settings import DIRECTORY_UI_PROFILE_URL

NAME = "Profile about"
SERVICE = "Single Sign-On"
TYPE = "profile"
URL = urljoin(DIRECTORY_UI_PROFILE_URL, "about/")
PAGE_TITLE = "Exporting is Great Account - GREAT.gov.uk"

EXPECTED_ELEMENTS = {
    "title": ".sso-profile-toolbar-labels-container > h1",
    "welcome message": "#welcome-message > h2",
}
SELECTORS = {}


def visit(driver: webdriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    check_title(driver, PAGE_TITLE, exact_match=False)
    check_for_expected_elements(driver, EXPECTED_ELEMENTS)
    logging.debug("All expected elements are visible on '%s' page", NAME)
