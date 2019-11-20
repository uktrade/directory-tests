# -*- coding: utf-8 -*-
"""Domestic - 2/4 page of Long SOO Contact us form"""
import logging
from types import ModuleType
from typing import Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType, common_selectors
from pages.common_actions import (
    Actor,
    Selector,
    assertion_msg,
    check_random_radio,
    check_url,
    fill_out_input_fields,
    find_element,
    submit_form,
    take_screenshot,
)
from pages.domestic import contact_us_soo_3_about_your_products

NAME = "About your business (SOO)"
SERVICE = Service.DOMESTIC
TYPE = PageType.FORM
URL = URLs.CONTACT_US_SOO_ORGANISATION_CONTACT_APPLICANT.absolute
PAGE_TITLE = "application - Selling Online Overseas -  great.gov.uk"

SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#content form"),
        "under £100,000": Selector(
            By.ID, "id_applicant-turnover_0", type=ElementType.RADIO, group_id=1
        ),
        "£100,000 to £500,000": Selector(
            By.ID, "id_applicant-turnover_1", type=ElementType.RADIO, group_id=1
        ),
        "£500,001 and £2million": Selector(
            By.ID, "id_applicant-turnover_2", type=ElementType.RADIO, group_id=1
        ),
        "more than £2million": Selector(
            By.ID, "id_applicant-turnover_3", type=ElementType.RADIO, group_id=1
        ),
        "company website": Selector(
            By.ID,
            "id_applicant-website_address",
            type=ElementType.INPUT,
            disabled=False,
        ),
        "submit": Selector(
            By.CSS_SELECTOR,
            "form button.button[type=submit]",
            type=ElementType.SUBMIT,
            next_page=contact_us_soo_3_about_your_products,
        ),
    }
}
SELECTORS.update(common_selectors.DOMESTIC_HEADER)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.DOMESTIC_FOOTER)


PREPOPULATED_FORM_FIELDS = {
    "company name": Selector(
        By.ID, "id_applicant-company_name", type=ElementType.INPUT, disabled=True
    ),
    "company number": Selector(
        By.ID, "id_applicant-company_number", type=ElementType.INPUT, disabled=True
    ),
    "address": Selector(
        By.ID, "id_applicant-company_address", type=ElementType.INPUT, disabled=True
    ),
    "company website": Selector(
        By.ID, "id_applicant-website_address", type=ElementType.INPUT, disabled=False
    ),
}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL)


def generate_form_details(actor: Actor, *, custom_details: dict = None) -> dict:
    result = {}

    if custom_details:
        result.update(custom_details)

    logging.debug(f"Generated form details: {result}")
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    check_random_radio(driver, form_selectors)
    fill_out_input_fields(driver, form_selectors, details)


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
            if existing_field_value.lower() == expected_value.lower():
                with assertion_msg(error):
                    assert existing_field_value.lower() == expected_value.lower()
                    logging.debug(
                        f"'{key}' field was prepopulated with expected value: "
                        f"'{expected_value}'"
                    )
            else:
                with assertion_msg(error):
                    assert existing_field_value.lower() in expected_value.lower()
                    logging.debug(
                        f"Prepopulated '{key}' field is part of expected value: "
                        f"'{expected_value}'"
                    )
