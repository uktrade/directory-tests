# -*- coding: utf-8 -*-
"""International - About UK page"""
import logging
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import common_selectors
from pages.common_actions import Selector, check_for_sections, check_url, go_to_url

NAME = "About the UK"
SERVICE = Service.INTERNATIONAL
TYPE = PageType.ARTICLE
URL = URLs.INTERNATIONAL_ABOUT_UK.absolute
PAGE_TITLE = "About the UK - great.gov.uk international"

SELECTORS = {
    "teaser": {
        "teaser section": Selector(By.CSS_SELECTOR, "#content section:nth-child(3)"),
    },
    "why choose the uk": {
        "why choose the uk section": Selector(
            By.CSS_SELECTOR, "#content section:nth-child(4)"
        ),
    },
    "uk industries": {
        "uk industries section": Selector(
            By.CSS_SELECTOR, "#content section:nth-child(5)"
        ),
    },
    "uk regions": {
        "uk regions section": Selector(
            By.CSS_SELECTOR, "#content section:nth-child(6)"
        ),
    },
    "how we help": {
        "how we help section": Selector(
            By.CSS_SELECTOR, "#content section:nth-child(7)"
        ),
    },
    "speak to us": {
        "speak to us section": Selector(
            By.CSS_SELECTOR, "#content section:nth-child(8)"
        ),
    },
}
SELECTORS.update(common_selectors.INTERNATIONAL_HEADER_WO_LANGUAGE_SELECTOR)
SELECTORS.update(common_selectors.INTERNATIONAL_HERO)
SELECTORS.update(common_selectors.ABOUT_UK_SUBHEADER)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.INTERNATIONAL_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL)
    logging.debug(f"All expected elements are visible on '{PAGE_TITLE}' page")


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)
