# -*- coding: utf-8 -*-
"""SSO Confirm Your Email Address Page Object."""
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared.enums import Service
from pages.common_actions import (
    Selector,
    check_url,
    find_element,
    take_screenshot,
    wait_for_page_load_after_action,
)
from directory_tests_shared.settings import SSO_URL

NAME = "Confirm your email address"
SERVICE = Service.SSO
TYPE = "confirmation"
URL = urljoin(SSO_URL, "accounts/confirm-email/")
PAGE_TITLE = "Confirm email Address"

CONFIRM_LINK = Selector(By.CSS_SELECTOR, "#content form > button[type=submit]")
SELECTORS = {
    "general": {
        "title": Selector(By.CSS_SELECTOR, "#content h1"),
        "confirm link": CONFIRM_LINK,
    }
}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)


def submit(driver: WebDriver):
    confirm_link = find_element(driver, CONFIRM_LINK)
    with wait_for_page_load_after_action(driver):
        confirm_link.click()
