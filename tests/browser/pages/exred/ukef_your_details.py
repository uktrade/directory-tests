# -*- coding: utf-8 -*-
"""ExRed UKEF Contact Us - Page Object."""
import logging
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Actor,
    Selector,
    check_url,
    fill_out_input_fields,
    find_element,
    go_to_url,
    take_screenshot,
)
from settings import EXRED_UI_URL

NAME = "Your details"
SERVICE = "Export Readiness"
TYPE = "UKEF Contact us"
URL = urljoin(EXRED_UI_URL, "get-finance/your-details/")
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
        "first name": Selector(
            By.ID, "id_your-details-firstname", type=ElementType.INPUT
        ),
        "last name": Selector(
            By.ID, "id_your-details-lastname", type=ElementType.INPUT
        ),
        "position": Selector(
            By.ID, "id_your-details-position", type=ElementType.INPUT
        ),
        "email": Selector(
            By.ID, "id_your-details-email", type=ElementType.INPUT
        ),
        "phone": Selector(
            By.ID, "id_your-details-phone", type=ElementType.INPUT
        ),
        "continue": SUBMIT_BUTTON,
    },
    "error reporting": {
        "itself": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "link": Selector(By.ID, "error-reporting-section-contact-us"),
    },
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def generate_form_details(actor: Actor) -> dict:
    result = {
        "first name": actor.alias,
        "last name": "automated tests",
        "position": "automated tests",
        "email": actor.email,
        "phone": "automated tests",
    }
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    fill_out_input_fields(driver, form_selectors, details)
    take_screenshot(driver, "After filling out the form")


def submit(driver: WebDriver):
    take_screenshot(driver, "Before submitting the form")
    button = find_element(
        driver, SUBMIT_BUTTON, element_name="Submit button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, "After submitting the form")
