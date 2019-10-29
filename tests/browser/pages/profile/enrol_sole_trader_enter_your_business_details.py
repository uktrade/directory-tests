# -*- coding: utf-8 -*-
"""Profile - Enrol - Enter your business details"""
import logging
import random
from collections import defaultdict
from types import ModuleType
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType
from pages.common_actions import (
    Actor,
    Selector,
    check_for_sections,
    check_url,
    fill_out_input_fields,
    find_and_click_on_page_element,
    find_elements_of_type,
    go_to_url,
    pick_option_from_autosuggestion,
    take_screenshot,
)
from pages.profile import enrol_enter_your_business_details_step_2
from pages.profile.autocomplete_callbacks import enrol_autocomplete_company_name

NAME = "Enter your business details (Sole trader or other type of business)"
SERVICE = Service.PROFILE
TYPE = PageType.FORM
URL = URLs.PROFILE_ENROL_NON_CH_COMPANY_ENTER_BUSINESS_DETAILS.absolute
PAGE_TITLE = ""

SELECTORS = {
    "enrolment progress bar": {"itself": Selector(By.ID, "progress-column")},
    "your business type": {
        "information box": Selector(By.ID, "business-type-information-box"),
        "change business type": Selector(By.ID, "change-business-type"),
    },
    "enter your business details": {
        "itself": Selector(By.CSS_SELECTOR, "section form"),
        "heading": Selector(By.CSS_SELECTOR, "#form-step-body-text h1"),
        "business category": Selector(
            By.ID, "id_address-search-company_type", type=ElementType.SELECT
        ),
        "business name": Selector(
            By.ID, "id_address-search-company_name", type=ElementType.INPUT
        ),
        "business postcode": Selector(
            By.ID,
            "id_postal_code",
            type=ElementType.INPUT,
            is_visible=False,
            autocomplete_callback=enrol_autocomplete_company_name,
        ),
        "industry": Selector(
            By.ID, "id_address-search-sectors", type=ElementType.SELECT
        ),
        "website": Selector(By.ID, "id_address-search-website", type=ElementType.INPUT),
        "submit": Selector(
            By.CSS_SELECTOR, "form button.button", type=ElementType.BUTTON
        ),
    },
}
FORM_FIELDS_WITH_USEFUL_DATA = {
    "company address": Selector(By.ID, "id_address", type=ElementType.TEXTAREA)
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def generate_form_details(actor: Actor) -> dict:
    postcodes = [
        "WC1N 3AX",
        "E13 0LD",
        "HP10 9AS",
        "IV30 5YE",
        "ML11 8AG",
        "RG26 5NW",
        "CB5 8SW",
        "W1W 7LJ",
        "LL69 9YN",
        "TN20 6HN",
    ]
    result = {
        "business category": None,
        "business name": "DIT AUTOMATED TESTS (delete me)",
        "business postcode": random.choice(postcodes),
        "industry": None,
        "website": "https://browser.tests.com",
    }
    logging.debug(f"Generated form details: {result}")
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["enter your business details"]
    pick_option_from_autosuggestion(driver, form_selectors, details)
    fill_out_input_fields(driver, form_selectors, details)
    take_screenshot(driver, "After filling out the form")


def submit(driver: WebDriver) -> ModuleType:
    take_screenshot(driver, "Before submitting the form")
    find_and_click_on_page_element(driver, SELECTORS, "submit", wait_for_it=False)
    take_screenshot(driver, "After submitting the form")
    return enrol_enter_your_business_details_step_2


def get_form_details(driver: WebDriver) -> dict:
    elements = find_elements_of_type(
        driver, FORM_FIELDS_WITH_USEFUL_DATA, ElementType.INPUT
    )
    result = defaultdict()
    for key, element in elements.items():
        value = element.get_attribute("value")
        result[key] = value

    return dict(result)
