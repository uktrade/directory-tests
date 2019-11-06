# -*- coding: utf-8 -*-
"""Regional landing page."""
import logging
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
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
TYPE = PageType.LANDING
URL = URLs.INTERNATIONAL_REGIONS.absolute
PAGE_TITLE = "Invest in Great Britain - "

SELECTORS = {
    "regions list": {
        "scotland": Selector(By.PARTIAL_LINK_TEXT, "Scotland"),
        "northern ireland": Selector(By.PARTIAL_LINK_TEXT, "Northern Ireland"),
        "north england": Selector(By.PARTIAL_LINK_TEXT, "North England"),
        "wales": Selector(By.PARTIAL_LINK_TEXT, "Wales"),
        "midlands": Selector(By.PARTIAL_LINK_TEXT, "Midlands"),
        "south england": Selector(By.PARTIAL_LINK_TEXT, "South England"),
    },
    "the uk map": {
        "the uk map - svg": Selector(By.CSS_SELECTOR, "svg.uk-map"),
        "scotland - svg": Selector(By.ID, "scotland"),
        "northern ireland - svg": Selector(By.ID, "northern-ireland"),
        "north england - svg": Selector(By.ID, "north-england"),
        "wales - svg": Selector(By.ID, "wales"),
        "midlands - svg": Selector(By.ID, "midlands"),
        "south england - svg": Selector(By.ID, "south-england"),
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
