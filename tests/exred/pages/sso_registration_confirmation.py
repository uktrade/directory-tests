# -*- coding: utf-8 -*-
"""SSO Registration Page Object."""
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import check_for_expected_elements, check_url
from settings import DIRECTORY_UI_SSO_URL
from utils import (
    find_element,
    take_screenshot,
    wait_for_page_load_after_action
)

NAME = "SSO Registration Confirmation page"
URL = urljoin(DIRECTORY_UI_SSO_URL, "accounts/confirm-email/")

SIGN_IN_LINK = "a.signin"
EXPECTED_ELEMENTS = {
    "title": "#content > div > div > h1",
    "description": "#content > div > div > p:nth-child(2)",
    "contact us link": "#content > div > div > p:nth-child(3) > a",
    "sign in link": SIGN_IN_LINK,
}


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    check_for_expected_elements(driver, EXPECTED_ELEMENTS)


def go_to_sign_in(driver: webdriver):
    registration_link = find_element(driver, by_css=SIGN_IN_LINK)
    with wait_for_page_load_after_action(driver):
        registration_link.click()
    take_screenshot(driver, NAME + "after signing in")
