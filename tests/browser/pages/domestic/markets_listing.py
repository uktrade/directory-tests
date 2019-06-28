# -*- coding: utf-8 -*-
"""Domestic Markets Page object"""

import logging
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType, Services, common_selectors
from pages.common_actions import Selector, check_url, go_to_url, take_screenshot
from pages.domestic import actions as domestic_actions
from settings import EXRED_UI_URL

NAME = "Markets"
SERVICE = Services.DOMESTIC
TYPE = "listing"
URL = urljoin(EXRED_UI_URL, "markets/")

SELECTORS = {
    "form": {
        "search box": Selector(By.ID, "search-box", type=ElementType.INPUT),
        "submit": Selector(
            By.CSS_SELECTOR,
            "#search-box ~ button[type=submit]",
            type=ElementType.BUTTON,
        ),
    },
    "no results": {"itself": Selector(By.ID, "search-results-list")},
}
SELECTORS.update(common_selectors.HEADER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def search(driver: WebDriver, phrase: str):
    domestic_actions.search(driver, phrase)
