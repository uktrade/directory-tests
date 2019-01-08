# -*- coding: utf-8 -*-
"""ExRed UKEF Contact Us - Page Object."""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Actor,
    Selector,
    check_url,
    find_element,
    go_to_url,
    take_screenshot,
    tick_checkboxes,
    check_for_sections
)
from settings import EXRED_UI_URL

NAME = "What would you like to know more about?"
SERVICE = "Export Readiness"
TYPE = "UKEF Contact us"
URL = urljoin(EXRED_UI_URL, "get-finance/contact/")
PAGE_TITLE = "Welcome to great.gov.uk"

BREADCRUMB_LINKS = Selector(By.CSS_SELECTOR, "div.breadcrumbs a")
SUBMIT_BUTTON = Selector(
    By.CSS_SELECTOR, "#content form button", type=ElementType.BUTTON
)
SELECTORS = {
    "breadcrumbs": {
        "itself": Selector(By.CSS_SELECTOR, "div.breadcrumbs"),
        "current page": Selector(
            By.CSS_SELECTOR, "div.breadcrumbs li[aria-current='page']"
        ),
        "links": BREADCRUMB_LINKS,
    },
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#content form"),
        "heading": Selector(By.CSS_SELECTOR, "#heading-container h2"),
        "securing upfront funding": Selector(
            By.ID,
            "checkbox-multiple-securing-upfront-funding-label",
            type=ElementType.CHECKBOX,
        ),
        "offering competitive but secure payment terms": Selector(
            By.ID,
            "checkbox-multiple-offering-competitive-but-secure-payment-terms-label",
            type=ElementType.CHECKBOX,
        ),
        "guidance on export finance and insurance": Selector(
            By.ID,
            "checkbox-multiple-guidance-on-export-finance-and-insurance-label",
            type=ElementType.CHECKBOX,
        ),
        "continue": SUBMIT_BUTTON,
    },
    "error reporting": {
        "itself": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "link": Selector(By.ID, "error-reporting-section-contact-us"),
    },
}


def visit(driver: WebDriver, *, page_name: str = None):
    go_to_url(driver, URL, page_name or NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def generate_form_details(actor: Actor) -> dict:
    result = {
        "securing upfront funding": True,
        "offering competitive but secure payment terms": True,
        "guidance on export finance and insurance": True,
    }
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    tick_checkboxes(driver, form_selectors, details)
    take_screenshot(driver, "After filling out the form")


def submit(driver: WebDriver):
    take_screenshot(driver, "Before submitting the form")
    button = find_element(
        driver, SUBMIT_BUTTON, element_name="Submit button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, "After submitting the form")
