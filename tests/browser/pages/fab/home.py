# -*- coding: utf-8 -*-
"""Find a Buyer Home Page Object."""
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import common_selectors
from pages.common_actions import Selector, check_url, go_to_url

NAME = "Home"
SERVICE = Service.FAB
TYPE = PageType.HOME
URL = URLs.FAB_LANDING.absolute
PAGE_TITLE = "Business profile - great.gov.uk"

SELECTORS = {
    "hero": {
        "hero": Selector(By.CSS_SELECTOR, "#content > section.great-hero-with-cta"),
        "start now": Selector(By.CSS_SELECTOR, "#content section:first-of-type a"),
    }
}
SELECTORS.update(common_selectors.DOMESTIC_HEADER)
SELECTORS.update(common_selectors.SSO_LOGGED_OUT)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.DOMESTIC_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", NAME)
