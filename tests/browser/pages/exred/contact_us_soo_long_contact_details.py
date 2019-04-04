# -*- coding: utf-8 -*-
"""SOO - First page of Long SOO Contact us form"""
import logging
import random
from types import ModuleType
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
    tick_captcha_checkbox,
    tick_checkboxes,
)
from pages.exred import contact_us_soo_long_thank_you
from settings import EXRED_UI_URL

NAME = "Long Domestic (Contact details)"
SERVICE = "Export Readiness"
TYPE = "Contact us"
URL = urljoin(EXRED_UI_URL, "contact/selling-online-overseas/contact-details/")
PAGE_TITLE = "Welcome to great.gov.uk"

SUBMIT_BUTTON = Selector(
    By.CSS_SELECTOR, "div.exred-triage-form button", type=ElementType.BUTTON
)
SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#content form"),
        "contact name": Selector(
            By.ID, "id_contact-details-contact_name", type=ElementType.INPUT
        ),
        "email address": Selector(
            By.ID, "id_contact-details-contact_email", type=ElementType.INPUT
        ),
        "telephone number": Selector(
            By.ID, "id_contact-details-phone", type=ElementType.INPUT
        ),
        "i prefer to be contacted by email": Selector(
            By.ID, "id_contact-details-email_pref", type=ElementType.CHECKBOX
        ),
        "t & c": Selector(
            By.ID, "id_contact-details-terms_agreed", type=ElementType.CHECKBOX
        ),
    }
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL)


def generate_form_details(actor: Actor) -> dict:
    prefer_email = random.choice([True, False])
    result = {
        "contact name": "automated tests",
        "email address": actor.email,
        "telephone number": "0700 100 2000",
        "i prefer to be contacted by email": prefer_email,
        "t & c": True,
    }
    logging.debug(f"Generated form details: {result}")
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    fill_out_input_fields(driver, form_selectors, details)
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
    return contact_us_soo_long_thank_you
