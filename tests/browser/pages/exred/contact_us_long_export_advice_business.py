# -*- coding: utf-8 -*-
"""Export Readiness - First page of Long Contact us form"""
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
from pages.exred import contact_us_short_domestic_thank_you
from settings import EXRED_UI_URL

NAME = "Long (Business details)"
SERVICE = "Export Readiness"
TYPE = "Contact us"
URL = urljoin(EXRED_UI_URL, "contact/export-advice/business/")
PAGE_TITLE = "Welcome to great.gov.uk"

SUBMIT_BUTTON = Selector(
    By.CSS_SELECTOR, "div.exred-triage-form button", type=ElementType.BUTTON
)
SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#lede form"),
        "uk private or public limited company": Selector(
            By.CSS_SELECTOR, "input[value='LIMITED']", type=ElementType.RADIO
        ),
        "other type of uk organisation": Selector(
            By.CSS_SELECTOR, "input[value='OTHER']", type=ElementType.RADIO
        ),
        "organisation name": Selector(
            By.ID, "id_business-organisation_name", type=ElementType.INPUT
        ),
        "postcode": Selector(By.ID, "id_business-postcode", type=ElementType.INPUT),
        "industry": Selector(By.ID, "id_business-industry", type=ElementType.SELECT),
        "turnover": Selector(By.ID, "id_business-turnover", type=ElementType.SELECT),
        "size": Selector(By.ID, "id_business-employees", type=ElementType.SELECT),
        "terms and conditions": Selector(
            By.ID, "id_business-terms_agreed", type=ElementType.CHECKBOX
        ),
    }
}

CH_NUMBER_SELECTORS = {
    "ch number": Selector(
        By.ID, "id_business-companies_house_number", type=ElementType.INPUT
    )
}
OTHER_SELECTORS = {
    "other": Selector(By.ID, "id_business-company_type_other", type=ElementType.SELECT)
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL)


def generate_form_details(actor: Actor) -> dict:
    is_company = random.choice([True, False])
    result = {
        "uk private or public limited company": is_company,
        "other type of uk organisation": not is_company,
        "organisation name": "automated tests",
        "postcode": "DIT",
        "industry": None,
        "turnover": None,
        "size": None,
        "terms and conditions": True,
    }
    if is_company:
        result.update({"ch number": "DIT"})
        SELECTORS["form"].update(CH_NUMBER_SELECTORS)
        # In order to avoid situation when previous scenario example modified
        # SELECTORS we have to remove OTHER_SELECTORS that were then added
        SELECTORS["form"] = dict(
            set(SELECTORS["form"].items()) - set(OTHER_SELECTORS.items())
        )
    else:
        SELECTORS["form"].update(OTHER_SELECTORS)
        SELECTORS["form"] = dict(
            set(SELECTORS["form"].items()) - set(CH_NUMBER_SELECTORS.items())
        )

    logging.debug(f"Generated form details: {result}")
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    check_radio(driver, form_selectors, details)
    fill_out_input_fields(driver, form_selectors, details)
    tick_checkboxes(driver, form_selectors, details)
    pick_option(driver, form_selectors, details)
    tick_captcha_checkbox(driver)
    take_screenshot(driver, "After filling out the form")


def submit(driver: WebDriver) -> ModuleType:
    take_screenshot(driver, "Before submitting the form")
    button = find_element(
        driver, SUBMIT_BUTTON, element_name="Submit button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, "After submitting the form")
    return contact_us_short_domestic_thank_you
