# -*- coding: utf-8 -*-
"""Export Readiness - Domestic Contact us - Great.gov.uk account"""
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Selector,
    check_url,
    find_and_click_on_page_element,
    go_to_url,
    take_screenshot,
)
from settings import EXRED_UI_URL

NAME = "Great.gov.uk account"
NAMES = [
    "I have not received an email confirmation",
    "I need to reset my password",
    "My Companies House login is not working",
    "I do not know where to enter my verification code",
    "I have not received my letter containing the verification code",
]
SERVICE = "Export Readiness"
TYPE = "Dedicated Support Content"
URL = urljoin(EXRED_UI_URL, "contact/triage/great-account/")
PAGE_TITLE = "Welcome to great.gov.uk"

URLs = {
    "great.gov.uk account": URL,
    "i have not received an email confirmation": urljoin(URL, "no-verification-email/"),
    "i need to reset my password": urljoin(URL, "password-reset/"),
    "my companies house login is not working": urljoin(URL, "companies-house-login/"),
    "i do not know where to enter my verification code": urljoin(
        URL, "verification-letter-code/"
    ),
    "i have not received my letter containing the verification code": urljoin(
        URL, "no-verification-letter/"
    ),
}

SUBMIT_BUTTON = Selector(
    By.CSS_SELECTOR, "form button[type=submit]", type=ElementType.BUTTON
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


def visit(driver: WebDriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: WebDriver, *, page_name: str = None):
    take_screenshot(driver, NAME)
    url = URLs[page_name.lower()] if page_name else URL
    check_url(driver, url, exact_match=False)
    msg = f"Got 404 on {driver.current_url}"
    assert "This page cannot be found" not in driver.page_source, msg


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)
