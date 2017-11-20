# -*- coding: utf-8 -*-
"""Find a Buyer Home Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from settings import DIRECTORY_UI_BUYER_URL
from utils import assertion_msg, take_screenshot

NAME = "Find a Buyer Home page"
URL = urljoin(DIRECTORY_UI_BUYER_URL, "")

EXPECTED_ELEMENTS = {
    "description": "#fabhome-intro > h1 > span:nth-child(1)",
    "company name input": "#fabhome-intro input[name='company_name']",
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
