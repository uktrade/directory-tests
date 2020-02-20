# -*- coding: utf-8 -*-
"""FAS - How we help you buy from the UK page."""
import logging
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType, common_selectors
from pages.common_actions import Selector, check_for_sections, check_url, go_to_url

NAME = "How we help you buy from the UK"
SERVICE = Service.INTERNATIONAL
TYPE = PageType.ARTICLE
URL = URLs.INTERNATIONAL_BUY_FROM_THE_UK.absolute
PAGE_TITLE = "How we help you buy from the UK - great.gov.uk international"

SELECTORS = {
    "teaser": {
        "teaser section": Selector(By.ID, "teaser-section"),
        "teaser description": Selector(By.CSS_SELECTOR, "#teaser-section p"),
    },
    "ebook": {
        "ebook section": Selector(By.ID, "ebook-section"),
        "ebook description": Selector(By.CSS_SELECTOR, "#ebook-section p"),
        "request your free brochure today": Selector(
            By.CSS_SELECTOR, "#ebook-section a", type=ElementType.LINK
        ),
    },
    "services": {
        "services section": Selector(By.ID, "services-fields-section"),
        "find a uk supplier": Selector(
            By.PARTIAL_LINK_TEXT, "Find a UK supplier", type=ElementType.LINK
        ),
        "make an introduction": Selector(
            By.PARTIAL_LINK_TEXT, "Get an introduction", type=ElementType.LINK
        ),
        "get advice": Selector(
            By.PARTIAL_LINK_TEXT, "Get advice", type=ElementType.LINK
        ),
        "find out more": Selector(
            By.PARTIAL_LINK_TEXT, "Find out more", type=ElementType.LINK
        ),
    },
    "contact us": {
        "contact us section": Selector(By.ID, "contact-us-section"),
        "get in touch": Selector(By.CSS_SELECTOR, "#contact-us-section a"),
    },
}
SELECTORS.update(common_selectors.INTERNATIONAL_HEADER_WO_LANGUAGE_SELECTOR)
SELECTORS.update(common_selectors.FAS_HEADER)
SELECTORS.update(common_selectors.INTERNATIONAL_HERO)
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
