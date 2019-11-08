# -*- coding: utf-8 -*-
"""Capital investment  - Thank you for your message page."""
import logging
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType, common_selectors
from pages.common_actions import (
    Selector,
    check_for_sections,
    check_url,
    go_to_url,
    take_screenshot,
)

NAME = "Thank you for contacting the Capital Investment team"
SERVICE = Service.INTERNATIONAL
TYPE = PageType.THANK_YOU
URL = URLs.INTERNATIONAL_CAPITAL_INVEST_CONTACT_SUCCESS.absolute
PAGE_TITLE = "Contact Form Success - great.gov.uk international"
SELECTORS = {
    "thank you message": {
        "message box": Selector(By.CSS_SELECTOR, "section div.message-box")
    },
    "what's next": {
        "what's next section": Selector(By.CSS_SELECTOR, "section.stone-page-section"),
        "capital investment in the uk": Selector(
            By.CSS_SELECTOR, "section.stone-page-section a", type=ElementType.LINK
        ),
    },
}
SELECTORS.update(common_selectors.INTERNATIONAL_HEADER)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.INTERNATIONAL_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, PAGE_TITLE)
    check_url(driver, URL, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)
