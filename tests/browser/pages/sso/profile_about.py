# -*- coding: utf-8 -*-
"""SSO Confirm Your Email Address Page Object."""
import logging
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
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

SELECTORS = {
    "general": {
        "title": Selector(
            By.CSS_SELECTOR, ".sso-profile-toolbar-labels-container > h1"
        ),
        "welcome message": Selector(By.CSS_SELECTOR, "#welcome-message > h2"),
    }
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", NAME)
