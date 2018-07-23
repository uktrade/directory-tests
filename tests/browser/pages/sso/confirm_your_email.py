# -*- coding: utf-8 -*-
"""SSO Confirm Your Email Address Page Object."""
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import (
    check_title,
    check_url,
    find_element,
    take_screenshot,
    wait_for_page_load_after_action,
)
from settings import DIRECTORY_UI_SSO_URL

NAME = "Confirm your email address"
SERVICE = "Single sign-on"
TYPE = "confirmation"
URL = urljoin(DIRECTORY_UI_SSO_URL, "accounts/confirm-email/")
PAGE_TITLE = "Confirm email Address"

CONFIRM_LINK = "#content > div > div > form > button"
EXPECTED_ELEMENTS = {"title": "#content > div > div > h1", "confirm link": CONFIRM_LINK}
SELECTORS = {}


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    check_title(driver, PAGE_TITLE, exact_match=False)


def submit(driver: webdriver):
    confirm_link = find_element(driver, by_css=CONFIRM_LINK)
    with wait_for_page_load_after_action(driver):
        confirm_link.click()
