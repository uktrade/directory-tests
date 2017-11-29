# -*- coding: utf-8 -*-
"""SSO Confirm Your Email Address Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from settings import DIRECTORY_UI_SSO_URL
from utils import assertion_msg, find_element, take_screenshot

NAME = "SSO Confirm your Email address page"
URL = urljoin(DIRECTORY_UI_SSO_URL, "accounts/confirm-email/")
PAGE_TITLE = "Confirm email Address"

CONFIRM_LINK = "#content > div > div > form > button"
EXPECTED_ELEMENTS = {
    "title": "#content > div > div > h1",
    "confirm link": CONFIRM_LINK,
}


def should_be_here(driver: webdriver):
    for element_name, element_selector in EXPECTED_ELEMENTS.items():
        element = find_element(driver, by_css=element_selector)
        with assertion_msg(
                "It looks like '%s' element is not visible on %s",
                element_name, NAME):
            assert element.is_displayed()
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def submit(driver: webdriver):
    confirm_link = find_element(driver, by_css=CONFIRM_LINK)
    confirm_link.click()
