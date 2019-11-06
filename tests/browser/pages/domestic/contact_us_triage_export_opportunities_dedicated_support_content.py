# -*- coding: utf-8 -*-
"""Domestic - Domestic Contact us - Great.gov.uk account"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType
from pages.common_actions import Selector, check_url, go_to_url, take_screenshot

NAME = "Export opportunities service"
NAMES = [
    "Export opportunities service",
    "I haven't had a response from the opportunity I applied for",
    "My daily alerts are not relevant to me",
]
SERVICE = Service.DOMESTIC
TYPE = PageType.DEDICATED_SUPPORT_CONTENT
URL = URLs.CONTACT_US_EXPORT_OPPORTUNITIES.absolute
PAGE_TITLE = "Welcome to great.gov.uk"

# fmt: off
SubURLs = {
    "export opportunities service": URL,
    "i haven't had a response from the opportunity i applied for":
        URLs.CONTACT_US_EXPORT_OPPORTUNITIES_NO_RESPONSE.absolute,
    "my daily alerts are not relevant to me":
        URLs.CONTACT_US_EXPORT_OPPORTUNITIES_NOT_RELEVANT.absolute,
}
# fmt: on

SUBMIT_BUTTON = Selector(
    By.CSS_SELECTOR, "div.exred-triage-form button", type=ElementType.BUTTON
)
SELECTORS = {
    "breadcrumbs": {
        "itself": Selector(By.CSS_SELECTOR, "div.breadcrumbs"),
        "links": Selector(By.CSS_SELECTOR, "div.breadcrumbs a"),
    },
    "support content": {
        "itself": Selector(By.CSS_SELECTOR, "div.container section"),
        "heading": Selector(By.CSS_SELECTOR, "section h1"),
        "content": Selector(By.CSS_SELECTOR, "section p"),
        "submit an enquiry": Selector(
            By.CSS_SELECTOR, "#further-help-link > a", type=ElementType.LINK
        ),
    },
    "error reporting": {
        "itself": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "link": Selector(By.ID, "error-reporting-section-contact-us"),
    },
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver, *, page_name: str = None):
    take_screenshot(driver, NAME)
    url = SubURLs[page_name.lower()] if page_name else URL
    check_url(driver, url, exact_match=False)
    msg = f"Got 404 on {driver.current_url}"
    assert "This page cannot be found" not in driver.page_source, msg
