# -*- coding: utf-8 -*-
"""Selling Online Overseas - Marketplace details page."""
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import Service
from pages import ElementType, common_selectors
from pages.common_actions import (
    Selector,
    check_for_sections,
    check_url,
    find_and_click_on_page_element,
    take_screenshot,
)

SERVICE = Service.SOO
TYPE = "search"
NAME = "Marketplace"
URL = URLs.SOO_MARKET_DETAILS.absolute
PAGE_TITLE = "Marketplace details | Selling Online Overseas"


SELECTORS = {
    "logo": {"logo": Selector(By.CSS_SELECTOR, "div.market-detail-logo img")},
    "apply now - sidebar": {"sidebar": Selector(By.CSS_SELECTOR, "div.aside-content")},
    "market details": {
        "marketplace": Selector(By.CSS_SELECTOR, "div.market-item h1"),
        "apply now": Selector(By.CSS_SELECTOR, "#content div.market-item a.button "),
    },
    "back": {
        "go back": Selector(
            By.CSS_SELECTOR, "#back-btn-container a", type=ElementType.LINK
        )
    },
    "breadcrumbs": {
        "itself": Selector(By.CSS_SELECTOR, ".breadcrumbs"),
        "current page": Selector(By.CSS_SELECTOR, "p.breadcrumbs > a:nth-child(4)"),
        "links": Selector(By.CSS_SELECTOR, ".breadcrumbs a"),
    },
}
SELECTORS.update(common_selectors.HEADER)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.FOOTER)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)


def click_on_page_element(driver, element_name):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)
