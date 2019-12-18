# -*- coding: utf-8 -*-
"""Domestic Empty Search Page object"""
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType
from pages.common_actions import Selector, check_url

NAME = "Empty Search results"
SERVICE = Service.DOMESTIC
TYPE = PageType.SEARCH
URL = URLs.DOMESTIC_SEARCH.absolute

SELECTORS = {
    "form": {
        "search box": Selector(By.ID, "search-box", type=ElementType.INPUT),
        "submit": Selector(
            By.CSS_SELECTOR,
            "#search-box ~ button[type=submit]",
            type=ElementType.BUTTON,
        ),
    },
    "results": {"itself": Selector(By.ID, "search-results-list")},
}


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)
