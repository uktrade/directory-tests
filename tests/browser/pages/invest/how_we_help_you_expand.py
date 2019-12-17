# -*- coding: utf-8 -*-
"""Invest - How we help you expand."""
import logging
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType, common_selectors
from pages.common_actions import Selector, check_for_sections, check_url, go_to_url

NAME = "How we help you expand"
SERVICE = Service.INVEST
TYPE = PageType.CONTENT
URL = URLs.INVEST_HOW_WE_HELP_EXPAND.absolute
PAGE_TITLE = "How we help you expand - great.gov.uk international"

SELECTORS = {
    "how we help": {
        "how we help section": Selector(By.ID, "services-fields-section"),
        "cards": Selector(
            By.CSS_SELECTOR, "#services-fields-section div.column-third-xl"
        ),
        "cards - icons": Selector(
            By.CSS_SELECTOR, "#services-fields-section div.column-third-xl img"
        ),
        "cards - headings": Selector(
            By.CSS_SELECTOR, "#services-fields-section div.column-third-xl h2"
        ),
        "cards - text": Selector(
            By.CSS_SELECTOR, "#services-fields-section div.column-third-xl p"
        ),
        "cards - links": Selector(
            By.CSS_SELECTOR, "#services-fields-section div.column-third-xl a"
        ),
        "speak to us": Selector(By.PARTIAL_LINK_TEXT, "Speak to us"),
        "explore industries": Selector(By.PARTIAL_LINK_TEXT, "Explore industries"),
        "find high-growth opportunities": Selector(
            By.PARTIAL_LINK_TEXT, "Find high-growth opportunities"
        ),
        "read our simple set-up guides": Selector(
            By.PARTIAL_LINK_TEXT, "Read our simple set-up guides"
        ),
        "search investment support directory": Selector(
            By.PARTIAL_LINK_TEXT, "Search Investment Support Directory"
        ),
        "get an introduction": Selector(By.PARTIAL_LINK_TEXT, "Get an introduction"),
        "get in touch": Selector(By.PARTIAL_LINK_TEXT, "Get in touch"),
        "discover the global entrepreneur programme": Selector(
            By.PARTIAL_LINK_TEXT, "Discover the Global Entrepreneur Programme"
        ),
        "get ongoing support": Selector(By.PARTIAL_LINK_TEXT, "Get ongoing support"),
    },
    "speak to us": {
        "speak to us section": Selector(By.ID, "contact-us-section"),
        "heading": Selector(By.CSS_SELECTOR, "#contact-us-section h2"),
        "text": Selector(By.CSS_SELECTOR, "#contact-us-section p"),
        "get in touch": Selector(
            By.CSS_SELECTOR, "#contact-us-section a", type=ElementType.LINK
        ),
    },
}
SELECTORS.update(common_selectors.INVEST_HEADER)
SELECTORS.update(common_selectors.INVEST_HERO)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.INVEST_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)
