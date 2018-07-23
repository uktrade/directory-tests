# -*- coding: utf-8 -*-
"""Find a Supplier - Generic Company Profile Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import (
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
    "name": {"itself": "#content h1.company-name-title"},
    "company details": {
        "itself": "#company-details",
        "logo": "#company-logo",
        "contact": "div.company-profile-module-details",
        "facts & details": "div.company-profile-module-facts",
    },
    "description": {
        "itself": "div.company-profile-module-description",
        "read full profile": "div.company-profile-module-description a",
    },
    "core industry": {"itself": "div.company-profile-industries"},
    "keywords": {"itself": "div.company-profile-keywords"},
    "report profile": {
        "itself": "div.ed-report-profile-container",
        "report profile": "div.ed-report-profile-container a[href^=mailto]",
    },
    "contact company": {
        "itself": "div.ed-contact-company-container",
        "contact company": "div.ed-contact-company-container a",
    },
}

OPTIONAL_SECTIONS = {
    "online profiles": {"itself": "div.company-profile-module-social-links"},
    "recent projects": {"itself": "#company-projects"},
}


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    check_for_expected_sections_elements(driver, SELECTORS)
    logging.debug("All expected elements are visible on '%s' page", NAME)
