# -*- coding: utf-8 -*-
"""Export Opportunities Home Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from settings import EXPORT_OPPORTUNITIES_UI_URL
from utils import assertion_msg, take_screenshot

NAME = "Export Opportunities Home page"
URL = urljoin(EXPORT_OPPORTUNITIES_UI_URL, "")

EXPECTED_ELEMENTS = {
    "title": "#content-top > div.hero__specialContainer > h1",
    "what product or service are you selling input": "#searchinput",
    "where would you like to sell to input": "#search-form input[placeholder='Filter by country']",
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
