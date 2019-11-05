# -*- coding: utf-8 -*-
"""SOO - First page of Long SOO Contact us form"""
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
    fill_out_input_fields,
    go_to_url,
    submit_form,
    take_screenshot,
    tick_captcha_checkbox,
    tick_checkboxes,
)
from pages.domestic import contact_us_soo_long_thank_you

NAME = "Long Domestic (Contact details)"
SERVICE = Service.DOMESTIC
TYPE = PageType.CONTACT_US
URL = URLs.CONTACT_US_SOO_ORGANISATION_CONTACT_DETAILS.absolute
PAGE_TITLE = "Welcome to great.gov.uk"

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
        "submit": Selector(
            By.CSS_SELECTOR,
            "div.exred-triage-form button",
            type=ElementType.SUBMIT,
            next_page=contact_us_soo_long_thank_you,
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


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
