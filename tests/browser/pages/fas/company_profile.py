# -*- coding: utf-8 -*-
"""Find a Supplier - Generic Company Profile Page Object."""
import logging
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    check_for_expected_sections_elements,
    check_url,
    take_screenshot,
)
from settings import DIRECTORY_UI_SUPPLIER_URL

NAME = "Company Profile"
SERVICE = "Find a Supplier"
TYPE = "profile"
URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "suppliers/")

SELECTORS = {
    "name": {"itself": Selector(By.CSS_SELECTOR, "#content h1.company-name-title")},
    "company details": {
        "itself": Selector(By.ID, "company-details"),
        "logo": Selector(By.ID, "company-logo"),
        "contact": Selector(By.CSS_SELECTOR, "div.company-profile-module-details"),
        "facts & details": Selector(
            By.CSS_SELECTOR, "div.company-profile-module-facts"
        ),
    },
    "description": {
        "itself": Selector(By.CSS_SELECTOR, "div.company-profile-module-description"),
        "read full profile": Selector(
            By.CSS_SELECTOR, "div.company-profile-module-description a"
        ),
    },
    "core industry": {
        "itself": Selector(By.CSS_SELECTOR, "div.company-profile-industries")
    },
    "keywords": {"itself": Selector(By.CSS_SELECTOR, "div.company-profile-keywords")},
    "report profile": {
        "itself": Selector(By.CSS_SELECTOR, "div.ed-report-profile-container"),
        "report profile": Selector(
            By.CSS_SELECTOR, "div.ed-report-profile-container a[href^=mailto]"
        ),
    },
    "contact company": {
        "itself": Selector(By.CSS_SELECTOR, "div.ed-contact-company-container"),
        "contact company": Selector(
            By.CSS_SELECTOR, "div.ed-contact-company-container a"
        ),
    },
}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    check_for_expected_sections_elements(driver, SELECTORS)
    logging.debug("All expected elements are visible on '%s' page", NAME)
