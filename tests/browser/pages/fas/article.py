# -*- coding: utf-8 -*-
"""Find a Supplier - Generic Article Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import (
    check_for_expected_sections_elements,
    check_url,
    take_screenshot,
)
from settings import DIRECTORY_UI_SUPPLIER_URL

NAME = "Find a Supplier - Article page"
URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "industry-articles/")

SECTIONS = {
    "breadcrumbs": {
        "itself": "p.breadcrumbs",
        "home": "p.breadcrumbs a[href='/']",
    },
    "article": {
        "itself": "#industry-article-container",
        "header": "#industry-article-container h1",
    },
    "contact us": {
        "itself": "#contact-area",
        "call to action": "#contact-area p",
        "contact us link": "#contact-area a",
    },
    "share on social media": {
        "itself": "ul.sharing-links",
        "twitter": "#share-twitter",
        "facebook": "#share-facebook",
        "linkedin": "#share-linkedin",
        "email": "#share-email",
    },
}


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    check_for_expected_sections_elements(driver, SECTIONS)
    logging.debug("All expected elements are visible on '%s' page", NAME)
