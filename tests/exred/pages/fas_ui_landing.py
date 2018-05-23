# -*- coding: utf-8 -*-
"""Find a Supplier Home Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import check_title, check_url, go_to_url, \
    check_for_expected_sections_elements
from settings import DIRECTORY_UI_SUPPLIER_URL
from utils import take_screenshot

NAME = "Find a Supplier Home page"
URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "")
PAGE_TITLE = \
    "Find trade profiles of reliable UK suppliers - trade.great.gov.uk"

SECTIONS = {
    "hero": {
        "itself": "section#hero",
    },
    "find uk suppliers": {
        "itself": "#search-area",
        "search term input": "#id_term",
        "search selectors dropdown": "#id_sectors",
        "find suppliers button": "#search-area > form button"
    },
    "contact us": {
        "itself": "#introduction-section",
        "introduction text": "#introduction-section p",
        "contact us button": "#introduction-section a"
    },
    "uk industries": {
        "itself": "#industries-section",
        "first industry": "#industries-section a:nth-child(1)",
        "second industry": "#industries-section a:nth-child(2)",
        "third industry": "#industries-section a:nth-child(3)",
        "see more button": "#industries-section > div > a.button"
    },
    "uk services": {
        "itself": "#services-section",
        "first service": "#services-section div.column-one-quarter:nth-child(3)",
        "second service": "#services-section div.column-one-quarter:nth-child(4)",
        "third service": "#services-section div.column-one-quarter:nth-child(5)",
        "fourth service": "#services-section div.column-one-quarter:nth-child(6)",
    }
}


def visit(driver: webdriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    check_title(driver, PAGE_TITLE, exact_match=True)
    check_for_expected_sections_elements(driver, SECTIONS)
    logging.debug("All expected elements are visible on '%s' page", NAME)
