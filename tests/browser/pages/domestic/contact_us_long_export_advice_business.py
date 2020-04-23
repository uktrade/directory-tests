# -*- coding: utf-8 -*-
"""Domestic - First page of Long Contact us form"""
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
    check_radio,
    check_url,
    fill_out_input_fields,
    go_to_url,
    pick_option,
    submit_form,
    tick_captcha_checkbox,
    tick_checkboxes,
)
from pages.domestic import contact_us_short_domestic_thank_you

NAME = "Long (Business details)"
SERVICE = Service.DOMESTIC
TYPE = PageType.CONTACT_US
URL = URLs.CONTACT_US_EXPORT_ADVICE_BUSINESS.absolute
PAGE_TITLE = "Welcome to great.gov.uk"

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
        "by mail": Selector(
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
        "submit": Selector(
            By.CSS_SELECTOR,
            "div.exred-triage-form button",
            type=ElementType.SUBMIT,
            next_page=contact_us_short_domestic_thank_you,
        ),
    }
}

OTHER_SELECTORS = {
    "other": Selector(By.ID, "id_business-company_type_other", type=ElementType.SELECT)
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL)


def generate_form_details(actor: Actor) -> dict:
    is_company = random.choice([True, False])
    by_email = random.choice([True, False])
    result = {
        "uk private or public limited company": is_company,
        "other type of uk organisation": not is_company,
        "organisation name": "automated tests",
        "postcode": "DIT",
        "industry": None,
        "turnover": None,
        "size": None,
        "by email": by_email,
        "by phone": random.choice([True, False]) if by_email else True,
    }
    if is_company:
        # In order to avoid situation when previous scenario example modified
        # SELECTORS we have to remove OTHER_SELECTORS that were then added
        SELECTORS["form"] = dict(
            set(SELECTORS["form"].items()) - set(OTHER_SELECTORS.items())
        )
    else:
        SELECTORS["form"].update(OTHER_SELECTORS)

    logging.debug(f"Generated form details: {result}")
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    check_radio(driver, form_selectors, details)
    fill_out_input_fields(driver, form_selectors, details)
    tick_checkboxes(driver, form_selectors, details)
    pick_option(driver, form_selectors, details)
    tick_captcha_checkbox(driver)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
