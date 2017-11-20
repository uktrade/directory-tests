# -*- coding: utf-8 -*-
"""Events Home Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from settings import EVENTS_UI_URL
from utils import assertion_msg, take_screenshot

NAME = "Events Home page"
URL = urljoin(EVENTS_UI_URL, "")

EXPECTED_ELEMENTS = {
    "title": "#feature div.pad > h2",
    "home button": "#filters > div.view-tabs > ul > li > a[title='Home']",
    "search input": "#fter[type='text']",
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
