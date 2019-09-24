# -*- coding: utf-8 -*-
"""Regional landing page."""
import logging
from typing import List
from urllib.parse import urljoin

from directory_tests_shared.enums import Service
from directory_tests_shared.settings import INTERNATIONAL_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import common_selectors
from pages.common_actions import (
    Selector,
    check_for_sections,
    check_url,
    find_and_click_on_page_element,
    take_screenshot,
    visit_url,
)

NAME = "Regions"
SERVICE = Service.INTERNATIONAL
TYPE = "landing"
URL = urljoin(INTERNATIONAL_URL, "content/about-uk/regions/")
PAGE_TITLE = "Invest in Great Britain - "

SELECTORS = {
    "the uk map": {
        "the uk map": Selector(By.CSS_SELECTOR, "svg.uk-map"),
        "scotland": Selector(By.ID, "scotland"),
        "northern ireland": Selector(By.ID, "northern-ireland"),
        "north england": Selector(By.ID, "north-england"),
        "wales": Selector(By.ID, "wales"),
        "midlands": Selector(By.ID, "midlands"),
        "south england": Selector(By.ID, "south-england"),
        "region links": Selector(By.CSS_SELECTOR, "a.region-link"),
    },
    "contact us": {"get in touch": Selector(By.PARTIAL_LINK_TEXT, "Get in touch")},
}
SELECTORS.update(common_selectors.INTERNATIONAL_HEADER_WO_LANGUAGE_SELECTOR)
SELECTORS.update(common_selectors.INTERNATIONAL_HERO)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.INTERNATIONAL_FOOTER)


def visit(driver: WebDriver):
    visit_url(driver, URL)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, PAGE_TITLE)
    check_url(driver, URL)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, PAGE_TITLE + " after clicking on " + element_name)
