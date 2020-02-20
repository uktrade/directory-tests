# -*- coding: utf-8 -*-
"""International - Transition period enquiries - Thank you page"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages.common_actions import Selector, check_url, go_to_url

NAME = "Transition period enquiries"
SERVICE = Service.INTERNATIONAL
TYPE = PageType.THANK_YOU
URL = URLs.CONTACT_US_INTERNATIONAL_TRANSITION_PERIOD_CONTACT_SUCCESS.absolute
PAGE_TITLE = "Welcome to great.gov.uk - buy from or invest in the UK"


LANGUAGE_SELECTOR = Selector(
    By.CSS_SELECTOR, "#international-header-bar .LanguageSelectorDialog-Tracker"
)
SUBMIT_BUTTON = Selector(By.CSS_SELECTOR, "form[method=POST] button")
SELECTORS = {
    "header bar": {"itself": Selector(By.ID, "international-header-bar")},
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


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=False)
