# -*- coding: utf-8 -*-
"""Domestic UKEF Contact Us - Page Object."""
import logging
from urllib.parse import urljoin

from directory_tests_shared.enums import Service
from directory_tests_shared.settings import DOMESTIC_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import Selector, check_url, go_to_url, take_screenshot

NAME = "Thank you"
SERVICE = Service.DOMESTIC
TYPE = "UKEF Contact us"
URL = urljoin(DOMESTIC_URL, "get-finance/contact/thanks/")
PAGE_TITLE = "Welcome to great.gov.uk"

SUBMIT_BUTTON = Selector(
    By.CSS_SELECTOR, "#content form button", type=ElementType.BUTTON
)
SELECTORS = {
    "breadcrumbs": {
        "itself": Selector(By.CSS_SELECTOR, "nav.breadcrumbs"),
        "current page": Selector(
            By.CSS_SELECTOR, "nav.breadcrumbs li[aria-current='page']"
        ),
        "links": Selector(By.CSS_SELECTOR, "nav.breadcrumbs a"),
    },
    "thank you": {
        "itself": Selector(By.ID, "success-message-container"),
        "heading": Selector(By.CSS_SELECTOR, "#success-message-container h1"),
        "home": Selector(By.CSS_SELECTOR, ".grid-row a", type=ElementType.LINK),
    },
    "error reporting": {
        "itself": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "link": Selector(By.ID, "error-reporting-section-contact-us"),
    },
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", NAME)
