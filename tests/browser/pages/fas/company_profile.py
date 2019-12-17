# -*- coding: utf-8 -*-
"""Find a Supplier - Generic Company Profile Page Object."""
import logging
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import common_selectors
from pages.common_actions import Selector, check_for_sections, check_url

NAME = "Company Profile"
SERVICE = Service.FAS
TYPE = PageType.PROFILE
URL = URLs.FAS_SUPPLIER.absolute

SELECTORS = {
    "name": {"itself": Selector(By.ID, "company-name")},
    "company details": {
        "itself": Selector(By.ID, "main-content"),
        "logo": Selector(By.ID, "cover-image-container"),
        "contact company": Selector(By.CSS_SELECTOR, "#contact-company-container a"),
        "about company": Selector(By.ID, "about-company-container"),
    },
    "online-profiles": {"itself": Selector(By.ID, "online-profiles")},
    "description": {
        "itself": Selector(By.ID, "company-description-container"),
        "read more": Selector(By.CSS_SELECTOR, "#company-description-container a"),
    },
}
SELECTORS.update(common_selectors.INTERNATIONAL_HEADER_WO_LANGUAGE_SELECTOR)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.INTERNATIONAL_FOOTER)


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)
