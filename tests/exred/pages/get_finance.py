# -*- coding: utf-8 -*-
"""Get Finance Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    WebDriverException
)

from settings import EXRED_UI_URL
from utils import assertion_msg, find_element, take_screenshot

NAME = "Get Finance Home page"
URL = urljoin(EXRED_UI_URL, "finance/get-finance-support-from-government")

EXPECTED_ELEMENTS = {
    "header": "#top > h1",
}

UNEXPECTED_ELEMENTS = {
    "share widget": "ul.sharing-links",
    "article counters and indicators": "#top > div.scope-indicator"
}


def should_be_here(driver: webdriver):
    for element_name, element_selector in EXPECTED_ELEMENTS.items():
        element = driver.find_element_by_css_selector(element_selector)
        with assertion_msg(
                "It looks like '%s' element is not visible on %s",
                element_name, NAME):
            assert element.is_displayed()

    for element_name, element_selector in UNEXPECTED_ELEMENTS.items():
        try:
            unexpected_element = find_element(driver, by_css=element_selector)
            with assertion_msg(
                    "It looks like '%s' element is visible on %s",
                    element_name, NAME):
                assert not unexpected_element.is_displayed()
        except (WebDriverException, NoSuchElementException):
            logging.debug("As expected '%s' is not present", element_name)

    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)
