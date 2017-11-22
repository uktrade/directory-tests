# -*- coding: utf-8 -*-
"""SSO Registration Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from settings import DIRECTORY_UI_SSO_URL
from utils import assertion_msg, find_element, take_screenshot

NAME = "SSO Registration Confirmation page"
URL = urljoin(DIRECTORY_UI_SSO_URL, "accounts/confirm-email/")

SIGN_IN_LINK = "header ul:nth-child(2) > li.float--left.soft-half--right > a"
EXPECTED_ELEMENTS = {
    "title": "#content > div > div > h1",
    "description": "#content > div > div > p:nth-child(2)",
    "contact us link": "#content > div > div > p:nth-child(3) > a",
    "sign in link": SIGN_IN_LINK,
}


def should_be_here(driver: webdriver):
    for element_name, element_selector in EXPECTED_ELEMENTS.items():
        element = driver.find_element_by_css_selector(element_selector)
        with assertion_msg(
                "It looks like '%s' element is not visible on %s",
                element_name, NAME):
            assert element.is_displayed()
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def go_to_sign_in(driver: webdriver):
    registration_link = find_element(driver, by_css=SIGN_IN_LINK)
    registration_link.click()
