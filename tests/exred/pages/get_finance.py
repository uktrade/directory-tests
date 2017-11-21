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

TOTAL_NUMBER_OF_ARTICLES = "dd.position > span.to"
ARTICLES_TO_READ_COUNTER = "dd.position > span.from"
TIME_TO_COMPLETE = "dd.time span.value"
SHARE_MENU = "ul.sharing-links"

EXPECTED_ELEMENTS = {
    "header": "#top > h1",
}

UNEXPECTED_ELEMENTS = {
    "share widget": "ul.sharing-links",
    "article counters and indicators": "#top > div.scope-indicator",
    "total number of articles": TOTAL_NUMBER_OF_ARTICLES,
    "articles read counter": ARTICLES_TO_READ_COUNTER,
    "time to complete remaining chapters": TIME_TO_COMPLETE,
    "share menu": SHARE_MENU,
}


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    for element_name, element_selector in EXPECTED_ELEMENTS.items():
        element = driver.find_element_by_css_selector(element_selector)
        with assertion_msg(
                "It looks like '%s' element is not visible on %s",
                element_name, NAME):
            assert element.is_displayed()
    logging.debug("All expected elements are visible on '%s' page", NAME)


def check_elements_are_not_visible(driver: webdriver, elements: list):
    take_screenshot(driver, NAME + " should not see some elements")
    for element in elements:
        selector = UNEXPECTED_ELEMENTS[element.lower()]
        try:
            page_element = driver.find_element_by_css_selector(selector)
            with assertion_msg(
                    "Expected not to see '%s' but we can see it", element):
                assert not page_element.is_displayed()
        except (WebDriverException, NoSuchElementException):
            logging.debug("As expected we can't see '%s' on the page", element)
