# -*- coding: utf-8 -*-
"""Domestic - Report a trade barrier page"""
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType, common_selectors
from pages.common_actions import (
    Selector,
    check_for_sections,
    check_url,
    go_to_url,
    take_screenshot,
)
from pages.domestic import actions as domestic_actions
from directory_tests_shared.enums import Service
from directory_tests_shared.settings import DOMESTIC_URL

NAME = "Report a trade barrier"
SERVICE = Service.DOMESTIC
TYPE = "article"
URL = urljoin(DOMESTIC_URL, "report-trade-barrier/")

SELECTORS = {
    "description": {
        "intro sections": Selector(By.CSS_SELECTOR, "p.lede"),
        "report a barrier": Selector(
            By.CSS_SELECTOR, "a.button", type=ElementType.LINK
        ),
        "contact the relevant british embassy": Selector(
            By.CSS_SELECTOR, "section div.grid-row p > a", type=ElementType.LINK
        ),
        "report steps": Selector(By.CSS_SELECTOR, "ol.list.big-number-list"),
    }
}
SELECTORS.update(common_selectors.HEADER)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def search(driver: WebDriver, phrase: str):
    domestic_actions.search(driver, phrase)
