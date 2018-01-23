# -*- coding: utf-8 -*-
"""Selling Online Overseas Home Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import go_to_url
from settings import SELLING_ONLINE_OVERSEAS_UI_URL
from utils import assertion_msg, find_element, take_screenshot

NAME = "Selling Online Overseas Home page"
URL = urljoin(SELLING_ONLINE_OVERSEAS_UI_URL, "")
PAGE_TITLE = "Welcome to Selling online overseas"

EXPECTED_ELEMENTS = {
    "title": "#content div.outer-container.soft-half--top.text-shadow > h1",
    "what do you sell input": "#search-product",
    "where do you want to sell input": "#search-country",
}


def visit(driver: webdriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: webdriver):
    with assertion_msg(
            "Expected page title to be: '%s' but got '%s'", PAGE_TITLE,
            driver.title):
        assert driver.title.lower() == PAGE_TITLE.lower()
    for element_name, element_selector in EXPECTED_ELEMENTS.items():
        element = find_element(driver, by_css=element_selector)
        with assertion_msg(
                "It looks like '%s' element is not visible on %s",
                element_name, NAME):
            assert element.is_displayed()
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)
