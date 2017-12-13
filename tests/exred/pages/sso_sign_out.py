# -*- coding: utf-8 -*-
"""SSO Sign Out Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from settings import DIRECTORY_UI_SSO_URL
from utils import assertion_msg, find_element, take_screenshot

NAME = "SSO Sign out page"
URL = urljoin(DIRECTORY_UI_SSO_URL, "accounts/logout/")

SIGN_OUT_BUTTON = "#content > div > div > form > button"
EXPECTED_ELEMENTS = {
    "title": "#content > div > div > h1",
    "sign in button": SIGN_OUT_BUTTON,
}


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    for element_name, element_selector in EXPECTED_ELEMENTS.items():
        element = find_element(driver, by_css=element_selector)
        with assertion_msg(
                "It looks like '%s' element is not visible on %s",
                element_name, NAME):
            assert element.is_displayed()
    logging.debug("All expected elements are visible on '%s' page", NAME)


def submit(driver: webdriver):
    sign_out_button = find_element(driver, by_css=SIGN_OUT_BUTTON)
    sign_out_button.click()
    take_screenshot(driver, NAME + "after signing out")
