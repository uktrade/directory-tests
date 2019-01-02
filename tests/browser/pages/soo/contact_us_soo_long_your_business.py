# -*- coding: utf-8 -*-
"""Export Readiness - First page of Long SOO Contact us form"""
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
    check_radio,
    check_url,
    fill_out_input_fields,
    find_element,
    go_to_url,
    pick_option,
    take_screenshot,
    tick_captcha_checkbox,
    tick_checkboxes,
)
from pages.soo import contact_us_soo_long_organisation_details
from settings import SELLING_ONLINE_OVERSEAS_UI_URL

NAME = "Long Domestic (Your Business)"
SERVICE = "Selling Online Overseas"
TYPE = "Contact us"
URL = urljoin(SELLING_ONLINE_OVERSEAS_UI_URL, "contact/selling-online-overseas/organisation/")
PAGE_TITLE = "Welcome to great.gov.uk"

SUBMIT_BUTTON = Selector(
    By.CSS_SELECTOR, "form button[type=submit]", type=ElementType.BUTTON
)
SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#content form"),
        "i don't have a company number": Selector(
            By.ID, "id_organisation-soletrader", type=ElementType.CHECKBOX
        ),
        "company name": Selector(
            By.ID, "id_organisation-company_name", type=ElementType.INPUT
        ),
        "company website": Selector(
            By.ID, "id_organisation-website_address", type=ElementType.INPUT
        ),
    }
}

OTHER_SELECTORS = {
    "postcode": Selector(
        By.ID, "id_organisation-company_postcode", type=ElementType.INPUT
    ),
}


def visit(driver: WebDriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL)


def generate_form_details(actor: Actor) -> dict:
    does_not_have_company_number = random.choice([True, False])
    result = {
        "i don't have a company number": does_not_have_company_number,
        "company name": "automated tests",
        "company website": "http://dit.automated.tests",
    }
    if does_not_have_company_number:
        result.update({"company postcode": "SW1H 0TL"})
        SELECTORS["form"].update(OTHER_SELECTORS)
    else:
        # In order to avoid situation when previous scenario example modified
        # SELECTORS we have to remove OTHER_SELECTORS that were then added
        SELECTORS["form"] = dict(
            set(SELECTORS["form"].items()) - set(OTHER_SELECTORS.items())
        )

    logging.debug(f"Generated form details: {result}")
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    tick_checkboxes(driver, form_selectors, details)
    fill_out_input_fields(driver, form_selectors, details)
    take_screenshot(driver, "After filling out the form")


def submit(driver: WebDriver) -> ModuleType:
    take_screenshot(driver, "Before submitting the form")
    button = find_element(
        driver, SUBMIT_BUTTON, element_name="Submit button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, "After submitting the form")
    return contact_us_soo_long_organisation_details
