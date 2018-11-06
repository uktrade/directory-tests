# -*- coding: utf-8 -*-
"""great.gov.uk International EU Exit Contact us - Thank you page"""
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    check_url,
    go_to_url,
    take_screenshot,
)
from settings import EXRED_UI_URL

NAME = "International EU Exit"
SERVICE = "Export Readiness"
TYPE = "Thank you for contacting us"
URL = urljoin(EXRED_UI_URL, "eu-exit/international/contact/success/")
PAGE_TITLE = "Welcome to great.gov.uk - buy from or invest in the UK"


LANGUAGE_SELECTOR = Selector(
    By.CSS_SELECTOR, "#international-header-bar .LanguageSelectorDialog-Tracker"
)
LANGUAGE_SELECTOR_CLOSE = Selector(By.ID, "header-language-selector-close")
BETA_FEEDBACK = Selector(By.CSS_SELECTOR, "#header-beta-bar span > a")
SUBMIT_BUTTON = Selector(By.CSS_SELECTOR, "form button")
SELECTORS = {
    "header bar": {
        "itself": Selector(By.ID, "international-header-bar"),
    },
    "header-menu": {
        "itself": Selector(By.ID, "international-header-menu"),
        "logo": Selector(By.ID, "international-header-logo"),
        "breadcrumbs": Selector(By.CSS_SELECTOR, ".breadcrumbs"),
    },
    "success": {
        "itself": Selector(By.ID, "success-message-container"),
        "header": Selector(By.CSS_SELECTOR, "#success-message-container h1"),
        "text": Selector(By.CSS_SELECTOR, "#success-message-container p"),
    },
    "what happens next": {
        "itself": Selector(By.ID, "next-container"),
        "header": Selector(By.CSS_SELECTOR, "#next-container h2"),
        "text": Selector(By.CSS_SELECTOR, "#next-container span"),
        "continue to great.gov.uk": Selector(By.CSS_SELECTOR, "#next-container a"),
    },
    "error reporting": {
        "itself": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "link": Selector(By.ID, "error-reporting-section-contact-us"),
    },
}


def visit(driver: WebDriver, *, page_name: str = None, first_time: bool = False):
    go_to_url(driver, URL, page_name, first_time=first_time)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
