# -*- coding: utf-8 -*-
"""Domestic - Country Guide page"""

import logging
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import Services, common_selectors
from pages.common_actions import Selector, check_url, go_to_url, take_screenshot
from pages.domestic import actions as domestic_actions
from settings import EXRED_UI_URL

NAME = "Markets"
SERVICE = Services.DOMESTIC
TYPE = "country guide"
URL = urljoin(EXRED_UI_URL, "markets/")

NAMES = [
    "Brazil",
    "China",
    "Denmark",
    "Germany",
    "Ireland",
    "Italy",
    "Japan",
    "Morocco",
    "South Korea",
    "The Netherlands",
    "Turkey",
]
URLs = {
    "brazil": urljoin(URL, "brazil/"),
    "china": urljoin(URL, "china/"),
    "denmark": urljoin(URL, "denmark/"),
    "germany": urljoin(URL, "germany/"),
    "ireland": urljoin(URL, "ireland/"),
    "italy": urljoin(URL, "italy/"),
    "japan": urljoin(URL, "japan/"),
    "morocco": urljoin(URL, "morocco/"),
    "south korea": urljoin(URL, "south-korea/"),
    "the netherlands": urljoin(URL, "netherlands/"),
    "turkey": urljoin(URL, "turkey/"),
}
SELECTORS = {
    "description": {
        "intro": Selector(By.ID, "country-guide-teaser-section"),
        "description": Selector(By.ID, "country-guide-section-one"),
        "statistics": Selector(By.ID, "country-guide-statistics-section"),
    },
    "opportunities for exporters": {
        "self": Selector(By.ID, "country-guide-section-two"),
        "accordions": Selector(By.ID, "country-guide-accordions"),
    },
    "doing business in": {"self": Selector(By.ID, "country-guide-section-three")},
    "next steps": {"self": Selector(By.ID, "country-guide-need-help-section")},
}
SELECTORS.update(common_selectors.HEADER)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.FOOTER)


def visit(driver: WebDriver, *, page_name: str = None):
    take_screenshot(driver, page_name or NAME)
    url = URLs[page_name.lower()] if page_name else URL
    go_to_url(driver, url, page_name or NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def search(driver: WebDriver, phrase: str):
    domestic_actions.search(driver, phrase)
