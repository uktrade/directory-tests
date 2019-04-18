# -*- coding: utf-8 -*-
"""ExRed Empty Search Page object"""

import logging
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import Selector, check_url, take_screenshot
from settings import EXRED_UI_URL

NAME = "Empty Search results"
SERVICE = "Export Readiness"
TYPE = "Search"
URL = urljoin(EXRED_UI_URL, "/search/?q=")

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
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)
