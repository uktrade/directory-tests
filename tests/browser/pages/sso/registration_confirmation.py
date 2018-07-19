# -*- coding: utf-8 -*-
"""SSO Registration Page Object."""
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    check_for_expected_elements,
    check_url,
    find_element,
    take_screenshot,
    wait_for_page_load_after_action,
)
from settings import DIRECTORY_UI_SSO_URL

NAME = "Registration Confirmation"
SERVICE = "Single Sign-On"
TYPE = "registration"
URL = urljoin(DIRECTORY_UI_SSO_URL, "accounts/confirm-email/")

SIGN_IN_LINK = Selector(By.CSS_SELECTOR, "a.signin")
SELECTORS = {
    "general": {
        "title": Selector(By.CSS_SELECTOR, "#content > div > div > h1"),
        "description": Selector(
            By.CSS_SELECTOR, "#content > div > div > p:nth-child(2)"
        ),
        "contact us link": Selector(
            By.CSS_SELECTOR, "#content > div > div > p:nth-child(3) > a"
        ),
        "sign in link": SIGN_IN_LINK,
    }
}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    check_for_expected_elements(driver, SELECTORS)


def go_to_sign_in(driver: WebDriver):
    registration_link = find_element(driver, SIGN_IN_LINK)
    with wait_for_page_load_after_action(driver):
        registration_link.click()
    take_screenshot(driver, NAME + "after signing in")
