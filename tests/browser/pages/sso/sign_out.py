# -*- coding: utf-8 -*-
"""SSO Sign Out Page Object."""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages.common_actions import (
    Selector,
    check_url,
    find_element,
    go_to_url,
    take_screenshot,
    wait_for_page_load_after_action,
)

NAME = "Sign out"
SERVICE = Service.SSO
TYPE = PageType.FORM
URL = URLs.SSO_LOGOUT.absolute
PAGE_TITLE = "Sign out - great.gov.uk"

SIGN_OUT_BUTTON = Selector(By.CSS_SELECTOR, "form button")
SELECTORS = {
    "general": {
        "title": Selector(By.CSS_SELECTOR, "#content h1.heading-xlarge"),
        "sign in button": SIGN_OUT_BUTTON,
    }
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)


def submit(driver: WebDriver):
    sign_out_button = find_element(
        driver, SIGN_OUT_BUTTON, element_name="Sign-out button"
    )
    with wait_for_page_load_after_action(driver):
        sign_out_button.click()
    take_screenshot(driver, NAME + "after signing out")
