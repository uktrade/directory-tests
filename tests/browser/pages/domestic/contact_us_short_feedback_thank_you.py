# -*- coding: utf-8 -*-
"""Domestic - Feedback Contact us form thank you page"""
import logging
import random
from types import ModuleType
from urllib.parse import urljoin
from uuid import uuid4

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType, Services
from pages.common_actions import (
    Actor,
    Selector,
    check_url,
    fill_out_input_fields,
    fill_out_textarea_fields,
    find_element,
    go_to_url,
    take_screenshot,
    tick_captcha_checkbox,
    tick_checkboxes,
)
from settings import EXRED_UI_URL

NAME = "Thank you for your feedback"
SERVICE = Services.DOMESTIC
TYPE = "Contact us"
URL = urljoin(EXRED_UI_URL, "contact/feedback/success/")
PAGE_TITLE = "Welcome to great.gov.uk"

SUBMIT_BUTTON = Selector(
    By.CSS_SELECTOR, "div.exred-triage-form button", type=ElementType.BUTTON
)
SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#lede form"),
        "full name": Selector(By.ID, "id_name", type=ElementType.INPUT),
        "email": Selector(By.ID, "id_email", type=ElementType.INPUT),
        "feedback": Selector(By.ID, "id_comment", type=ElementType.TEXTAREA),
        "terms and conditions": Selector(
            By.ID, "id_terms_agreed", type=ElementType.CHECKBOX
        ),
        "submit": SUBMIT_BUTTON,
    }
}
OTHER_SELECTORS = {
    "other": Selector(By.ID, "id_company_type_other", type=ElementType.SELECT)
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver, *, page_name: str = None):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)


def generate_form_details(actor: Actor) -> dict:
    result = {
        "full name": str(uuid4()),
        "email": actor.email,
        "feedback": f"Feedback submitted by automated tests {actor.alias}",
        "terms and conditions": True,
    }
    logging.debug(f"Generated form details: {result}")
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    fill_out_input_fields(driver, form_selectors, details)
    fill_out_textarea_fields(driver, form_selectors, details)
    tick_checkboxes(driver, form_selectors, details)
    tick_captcha_checkbox(driver)
    take_screenshot(driver, "After filling out the form")


def submit(driver: WebDriver) -> ModuleType:
    take_screenshot(driver, "Before submitting the form")
    button = find_element(
        driver, SUBMIT_BUTTON, element_name="Submit button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, "After submitting the form")
    return
