# -*- coding: utf-8 -*-
"""Domestic - SOO Domestic Long Contact us - Thank you for your enquiry."""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import common_selectors
from pages.common_actions import Selector, check_url, take_screenshot

NAME = "Thank you for your enquiry (SOO)"
SERVICE = Service.DOMESTIC
TYPE = PageType.CONTACT_US
URL = URLs.CONTACT_US_SOO_ORGANISATION_SUCCESS.absolute
PAGE_TITLE = "Welcome to great.gov.uk"

PDF_LINKS = Selector(By.CSS_SELECTOR, "#documents-section a.link")
SELECTORS = {
    "confirmation": {
        "itself": Selector(By.ID, "success-message-container"),
        "heading": Selector(By.CSS_SELECTOR, "#success-message-container h1"),
    }
}
SELECTORS.update(common_selectors.DOMESTIC_HEADER)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.DOMESTIC_FOOTER)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, PAGE_TITLE)
    check_url(driver, URL, exact_match=True)
