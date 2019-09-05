# -*- coding: utf-8 -*-
"""Find a Supplier - Thank you for your message Page Object."""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import Services, common_selectors
from pages.common_actions import (
    Selector,
    check_for_sections,
    check_url,
    take_screenshot,
)
from settings import DIRECTORY_UI_SUPPLIER_URL

NAME = "Thank you for your message"
SERVICE = Services.FIND_A_SUPPLIER
TYPE = "contact"
URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "industries/contact/")
PAGE_TITLE = "Contact us - trade.great.gov.uk"

SELECTORS = {
    "breadcrumbs": {"itself": Selector(By.CSS_SELECTOR, "p.breadcrumbs")},
    "message": {
        "itself": Selector(By.ID, "lede"),
        "header": Selector(By.CSS_SELECTOR, "#lede h2"),
        "go back link": Selector(By.CSS_SELECTOR, "#lede a"),
    },
}
SELECTORS.update(common_selectors.INTERNATIONAL_HEADER_WO_LANGUAGE_SELECTOR)
SELECTORS.update(common_selectors.INTERNATIONAL_FOOTER)


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=False)
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)
