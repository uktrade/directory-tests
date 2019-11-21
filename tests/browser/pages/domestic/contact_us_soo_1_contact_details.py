# -*- coding: utf-8 -*-
"""Domestic - 1/4 page of Long SOO Contact us form"""
import logging
import random
from types import ModuleType
from typing import Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from directory_tests_shared.utils import check_url_path_matches_template
from pages import ElementType, common_selectors
from pages.common_actions import (
    Actor,
    Selector,
    assertion_msg,
    fill_out_input_fields,
    find_element,
    go_to_url,
    submit_form,
    take_screenshot,
    tick_checkboxes,
)
from pages.domestic import contact_us_soo_2_about_your_business

NAME = "Contact details (SOO)"
SERVICE = Service.DOMESTIC
TYPE = PageType.CONTACT_US
URL = URLs.CONTACT_US_SOO_ORGANISATION_CONTACT_DETAILS.absolute_template
PAGE_TITLE = "Welcome to great.gov.uk"

SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#content form"),
        "phone number": Selector(
            By.ID, "id_contact-details-phone", type=ElementType.INPUT
        ),
        "contact by email": Selector(
            By.ID, "id_contact-details-email_pref", type=ElementType.CHECKBOX
        ),
        "submit": Selector(
            By.CSS_SELECTOR,
            "form button.button[type=submit]",
            type=ElementType.SUBMIT,
            next_page=contact_us_soo_2_about_your_business,
        ),
    }
}
SELECTORS.update(common_selectors.DOMESTIC_HEADER)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.DOMESTIC_FOOTER)

PREPOPULATED_FORM_FIELDS = {
    "first name": Selector(
        By.ID, "id_contact-details-contact_first_name", disabled=True
    ),
    "last name": Selector(By.ID, "id_contact-details-contact_last_name", disabled=True),
    "email": Selector(By.ID, "id_contact-details-contact_email", disabled=True),
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url_path_matches_template(URL, driver.current_url)


def generate_form_details(actor: Actor, *, custom_details: dict = None) -> dict:
    result = {
        "phone number": "0123456789",
        "contact by email": random.choice([True, False]),
    }

    if custom_details:
        result.update(custom_details)

    logging.debug(f"Generated form details: {result}")
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    fill_out_input_fields(driver, form_selectors, details)
    tick_checkboxes(driver, form_selectors, details)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])


def check_if_populated(driver: WebDriver, expected_form_details: dict):
    for key, expected_value in expected_form_details.items():
        existing_field_selector = PREPOPULATED_FORM_FIELDS.get(key, None)
        if not existing_field_selector:
            continue
        existing_field = find_element(driver, existing_field_selector, element_name=key)
        existing_field_value = existing_field.get_attribute("value")
        if expected_value:
            error = (
                f"Expected '{key}' value to be '{expected_value}' but got "
                f"'{existing_field_value}'"
            )
            with assertion_msg(error):
                assert existing_field_value.lower() == expected_value.lower()
                logging.debug(
                    f"'{key}' field was prepopulated with expected value: "
                    f"'{expected_value}'"
                )
