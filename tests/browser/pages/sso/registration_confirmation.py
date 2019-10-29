# -*- coding: utf-8 -*-
"""SSO Registration Page Object."""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages.common_actions import Selector, check_url, take_screenshot

NAME = "Registration Confirmation"
SERVICE = Service.SSO
TYPE = PageType.CONFIRMATION
URL = URLs.SSO_EMAIL_CONFIRM.absolute

SIGN_IN_LINK = Selector(By.ID, "header-sign-in-link")
SELECTORS = {
    "general": {
        "title": Selector(By.CSS_SELECTOR, "#content h1"),
        "description": Selector(By.CSS_SELECTOR, "#content p:nth-child(2)"),
        "contact us link": Selector(By.CSS_SELECTOR, "#content p > a"),
        "sign in link": SIGN_IN_LINK,
    }
}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
