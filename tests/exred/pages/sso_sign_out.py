# -*- coding: utf-8 -*-
"""SSO Sign Out Page Object."""
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import (
    check_for_expected_elements,
    check_title,
    check_url,
    go_to_url
)
from settings import DIRECTORY_UI_SSO_URL
from utils import (
    find_element,
    take_screenshot,
    wait_for_page_load_after_action
)

NAME = "SSO Sign out page"
URL = urljoin(DIRECTORY_UI_SSO_URL, "accounts/logout/")
PAGE_TITLE = "Sign out - great.gov.uk"

SIGN_OUT_BUTTON = "#content > div > div > form > button"
EXPECTED_ELEMENTS = {
    "title": "#content > div > div > h1",
    "sign in button": SIGN_OUT_BUTTON,
}


def visit(driver: webdriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    check_title(driver, PAGE_TITLE, exact_match=False)
    check_for_expected_elements(driver, EXPECTED_ELEMENTS)


def submit(driver: webdriver):
    sign_out_button = find_element(
        driver, by_css=SIGN_OUT_BUTTON, element_name="Sign-out button")
    with wait_for_page_load_after_action(driver):
        sign_out_button.click()
    take_screenshot(driver, NAME + "after signing out")
