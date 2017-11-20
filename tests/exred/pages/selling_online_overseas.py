# -*- coding: utf-8 -*-
"""Selling Online Overseas Home Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from settings import SELLING_ONLINE_OVERSEAS_UI_URL
from utils import assertion_msg, take_screenshot

NAME = "Selling Online Overseas Home page"
URL = urljoin(SELLING_ONLINE_OVERSEAS_UI_URL, "")

EXPECTED_ELEMENTS = {
    "title": "#content div.outer-container.soft-half--top.text-shadow > h1",
    "what do you sell input": "#search-product",
    "where do you want to sell input": "#search-country",
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
