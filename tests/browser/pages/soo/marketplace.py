# -*- coding: utf-8 -*-
"""Selling Online Overseas - Marketplace details page."""
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from directory_tests_shared.utils import check_url_path_matches_template
from pages import ElementType, common_selectors
from pages.common_actions import Selector, check_for_sections, take_screenshot

NAME = "Marketplace"
SERVICE = Service.SOO
TYPE = PageType.SEARCH
URL = URLs.SOO_MARKET_DETAILS.absolute_template
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
SELECTORS.update(common_selectors.DOMESTIC_HEADER)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.DOMESTIC_FOOTER)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url_path_matches_template(URL, driver.current_url)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)
