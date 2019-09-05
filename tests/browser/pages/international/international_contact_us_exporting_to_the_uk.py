# -*- coding: utf-8 -*-
"""International - Exporting to the UK contact us page"""
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType, Services, common_selectors
from pages.common_actions import (
    Selector,
    check_url,
    find_and_click_on_page_element,
    go_to_url,
    take_screenshot,
)
from settings import EXRED_UI_URL

NAME = "Exporting to the UK"
SERVICE = Services.INTERNATIONAL
TYPE = "Dedicated Support Content"
URL = urljoin(EXRED_UI_URL, "contact/triage/international/exporting-to-the-uk/")
PAGE_TITLE = "Welcome to great.gov.uk"

SUBMIT_BUTTON = Selector(
    By.CSS_SELECTOR, "div.exred-triage-form button", type=ElementType.BUTTON
)
SELECTORS = {
    "support content": {
        "itself": Selector(By.CSS_SELECTOR, "div.container section"),
        "heading": Selector(By.CSS_SELECTOR, "section h1"),
        "content": Selector(By.CSS_SELECTOR, "section p"),
        "what you need to do": Selector(By.CSS_SELECTOR, "section p a.link"),
        "continue to ask us a question": Selector(
            By.CSS_SELECTOR, "#further-help-link > a", type=ElementType.LINK
        ),
    }
}

SELECTORS.update(common_selectors.INTERNATIONAL_HEADER)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.INTERNATIONAL_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    msg = f"Got 404 on {driver.current_url}"
    assert "This page cannot be found" not in driver.page_source, msg


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)
