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
    check_url,
    fill_out_input_fields,
    find_element,
    go_to_url,
    take_screenshot,
    tick_checkboxes,
)
from pages.exred import contact_us_soo_long_organisation_details
from settings import EXRED_UI_URL

NAME = "Long Domestic (Your Business)"
SERVICE = "Export Readiness"
TYPE = "Contact us"
URL = urljoin(EXRED_UI_URL, "contact/selling-online-overseas/organisation/")
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
        "company website": Selector(
            By.ID, "id_organisation-website_address", type=ElementType.INPUT
        ),
    }
}

HAS_COMPANY_NUMBER = {
    "company name": Selector(
        By.ID, "id_organisation-company_name", type=ElementType.INPUT
    ),
}

DOESNT_HAVE_COMPANY_NUMBER = {
    "company postcode": Selector(
        By.ID, "id_organisation-company_postcode", type=ElementType.INPUT
    ),
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)


def generate_form_details(actor: Actor, *, custom_details: dict = None) -> dict:
    does_not_have_company_number = custom_details.get(
        "i don't have a company number", random.choice([True, False])
    )
    result = {
        "i don't have a company number": does_not_have_company_number,
        "company website":
            f"http://{actor.email}.automated.tests.com".replace("@", "."),
    }
    if does_not_have_company_number:
        result.update({"company postcode": "SW1H 0TL"})
        SELECTORS["form"].update(DOESNT_HAVE_COMPANY_NUMBER)
        SELECTORS["form"] = dict(
            set(SELECTORS["form"].items()) - set(HAS_COMPANY_NUMBER.items())
        )
    else:
        result.update({"company name": "automated tests"})
        SELECTORS["form"].update(HAS_COMPANY_NUMBER)
        # In order to avoid situation when previous scenario example modified
        # SELECTORS we have to remove OTHER_SELECTORS that were then added
        SELECTORS["form"] = dict(
            set(SELECTORS["form"].items()) - set(DOESNT_HAVE_COMPANY_NUMBER.items())
        )
    if custom_details:
        result.update(custom_details)

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
