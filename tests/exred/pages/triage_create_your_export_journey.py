# -*- coding: utf-8 -*-
"""Triage - Create your export journey Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from settings import EXRED_UI_URL
from utils import assertion_msg, find_element, take_screenshot

NAME = "Create your export journey"
URL = urljoin(EXRED_UI_URL, "custom/")
PAGE_TITLE = "Your export journey - great.gov.uk"

START_NOW = "#start-now-container > a"
REGISTER = "#start-now-container > div > a:nth-child(2)"
SIGN_IN = "#start-now-container > div > a:nth-child(3)"
REPORT_THIS_PAGE = "#error-reporting-section-contact-us"
EXPECTED_ELEMENTS = {
    "title": "#start-now-container > h1",
    "description": "#start-now-container > p:nth-child(3)",
    "list of benefits": "#start-now-container > ul",
    "start now": START_NOW,
    "register": REGISTER,
    "sign in": SIGN_IN,
    "report this page": REPORT_THIS_PAGE
}


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    with assertion_msg(
            "Expected page URL to be: '%s' but got '%s'", URL,
            driver.current_url):
        assert driver.current_url in URL
    with assertion_msg(
            "Expected page title to be: '%s' but got '%s'", PAGE_TITLE,
            driver.title):
        assert PAGE_TITLE.lower() in driver.title.lower()
    for element_name, element_selector in EXPECTED_ELEMENTS.items():
        element = driver.find_element_by_css_selector(element_selector)
        with assertion_msg(
                "It looks like '%s' element is not visible on %s",
                element_name, NAME):
            assert element.is_displayed()
    logging.debug("All expected elements are visible on '%s' page", NAME)


def start_now(driver: webdriver):
    star_now = find_element(driver, by_css=START_NOW)
    star_now.click()
    take_screenshot(driver, NAME)
