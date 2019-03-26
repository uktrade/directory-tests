# -*- coding: utf-8 -*-
"""Find a Supplier - Generic Article Page Object."""
import logging
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import Selector, check_url, take_screenshot
from settings import DIRECTORY_UI_SUPPLIER_URL

NAME = "Article"
SERVICE = "Find a Supplier"
TYPE = "article"
URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "industry-articles/")

SELECTORS = {
    "breadcrumbs": {
        "itself": Selector(By.CSS_SELECTOR, "p.breadcrumbs"),
        "home": Selector(By.CSS_SELECTOR, "p.breadcrumbs a[href='/']"),
    },
    "article": {
        "itself": Selector(By.ID, "industry-article-container"),
        "header": Selector(By.CSS_SELECTOR, "#industry-article-container h1"),
    },
    "contact us": {
        "itself": Selector(By.ID, "contact-area"),
        "call to action": Selector(By.CSS_SELECTOR, "#contact-area p"),
        "contact us link": Selector(By.CSS_SELECTOR, "#contact-area a"),
    },
    "share on social media": {
        "itself": Selector(By.CSS_SELECTOR, "ul.sharing-links"),
        "twitter": Selector(By.ID, "share-twitter"),
        "facebook": Selector(By.ID, "share-facebook"),
        "linkedin": Selector(By.ID, "share-linkedin"),
        "email": Selector(By.ID, "share-email"),
    },
}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)
