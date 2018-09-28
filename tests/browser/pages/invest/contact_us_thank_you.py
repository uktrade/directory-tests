# -*- coding: utf-8 -*-
"""Invest in Great - Thank you for your message Page Object."""
import logging
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    check_for_expected_sections_elements,
    check_title,
    check_url,
    Selector,
    take_screenshot,
    visit_url,
)
from settings import INVEST_UI_URL

NAME = "Thank you for your message"
SERVICE = "invest"
TYPE = "contact"
URL = urljoin(INVEST_UI_URL, "contact/success/")
PAGE_TITLE = ""
SELECTORS = {
    "hero": {
        "itself": Selector(By.CSS_SELECTOR, "section.hero"),
    },
    "success message": {
        "itself": Selector(By.CSS_SELECTOR, "section.contact-success")
    }
}


def visit(driver: WebDriver, *, first_time: bool = False):
    visit_url(driver, URL)


def should_be_here(driver: WebDriver):
    check_title(driver, PAGE_TITLE, exact_match=False)
    check_url(driver, URL, exact_match=True)
    take_screenshot(driver, PAGE_TITLE)
    check_for_expected_sections_elements(driver, SELECTORS)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)
