# -*- coding: utf-8 -*-
"""Domestic UKEF Contact Us - Page Object."""
import logging
import random
from types import ModuleType
from typing import Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType
from pages.common_actions import (
    Actor,
    Selector,
    check_url,
    fill_out_textarea_fields,
    go_to_url,
    submit_form,
    tick_captcha_checkbox,
    tick_checkboxes,
)

NAME = "Tell us how we can help"
SERVICE = Service.DOMESTIC
TYPE = PageType.UKEF_CONTACT_US
URL = URLs.DOMESTIC_GET_FINANCE_HELP.absolute
PAGE_TITLE = "Welcome to great.gov.uk"

BREADCRUMB_LINKS = Selector(By.CSS_SELECTOR, "div.breadcrumbs a")
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
        "comment": Selector(By.ID, "id_help-comment", type=ElementType.TEXTAREA),
        "by email": Selector(
            By.ID,
            "checkbox-multiple-i-would-like-to-receive-additional-information-by-email",
            type=ElementType.CHECKBOX,
            is_visible=False,
            alternative_visibility_check=True,
        ),
        "by phone": Selector(
            By.ID,
            "checkbox-multiple-i-would-like-to-receive-additional-information-by-telephone",
            type=ElementType.CHECKBOX,
            is_visible=False,
            alternative_visibility_check=True,
        ),
        "continue": Selector(
            By.CSS_SELECTOR, "#content form button", type=ElementType.SUBMIT
        ),
    },
    "error reporting": {
        "itself": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "link": Selector(By.ID, "error-reporting-section-contact-us"),
    },
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def generate_form_details(actor: Actor) -> dict:
    by_email = random.choice([True, False])
    result = {
        "comment": f"Submitted by automated tests {actor.email}",
        "by email": by_email,
        "by phone": random.choice([True, False]) if by_email else True,
    }
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    fill_out_textarea_fields(driver, form_selectors, details)
    tick_checkboxes(driver, form_selectors, details)
    tick_captcha_checkbox(driver)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
