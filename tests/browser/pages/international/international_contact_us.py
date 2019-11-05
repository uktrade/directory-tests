# -*- coding: utf-8 -*-
"""International - Contact us form"""
import logging
import random
from types import ModuleType
from typing import Union
from uuid import uuid4

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
    fill_out_textarea_fields,
    go_to_url,
    pick_option,
    submit_form,
    take_screenshot,
    tick_captcha_checkbox,
    tick_checkboxes,
)
from pages.domestic import contact_us_triage_domestic

NAME = "Contact us"
SERVICE = Service.INTERNATIONAL
TYPE = PageType.CONTACT_US
URL = URLs.CONTACT_US_FORM_INTERNATIONAL.absolute
PAGE_TITLE = "Welcome to great.gov.uk"

SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#lede form"),
        "first name": Selector(By.ID, "id_given_name", type=ElementType.INPUT),
        "last name": Selector(By.ID, "id_family_name", type=ElementType.INPUT),
        "email": Selector(By.ID, "id_email", type=ElementType.INPUT),
        "company": Selector(By.ID, "id_organisation_type_0", type=ElementType.CHECKBOX),
        "other type of organisation": Selector(
            By.ID, "id_organisation_type_1", type=ElementType.CHECKBOX
        ),
        "your organisation name": Selector(
            By.ID, "id_organisation_name", type=ElementType.INPUT
        ),
        "country": Selector(By.ID, "id_country_name", type=ElementType.SELECT),
        "city": Selector(By.ID, "id_city", type=ElementType.INPUT),
        "comment": Selector(By.ID, "id_comment", type=ElementType.TEXTAREA),
        "accept t&c": Selector(By.ID, "id_terms_agreed", type=ElementType.CHECKBOX),
        "submit": Selector(
            By.CSS_SELECTOR,
            "div.exred-triage-form button",
            type=ElementType.SUBMIT,
            next_page=contact_us_triage_domestic,
        ),
    }
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)


def generate_form_details(actor: Actor) -> dict:
    is_company = random.choice([True, False])
    result = {
        "first name": actor.alias,
        "last name": str(uuid4()),
        "email": actor.email,
        "company": is_company,
        "other type of organisation": not is_company,
        "your organisation name": "automated tests",
        "country": None,
        "city": "Automated tests",
        "comment": "This is a test message sent via automated tests",
        "accept t&c": True,
    }
    logging.debug(f"Generated form details: {result}")
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["enter your details form"]
    fill_out_input_fields(driver, form_selectors, details)
    fill_out_textarea_fields(driver, form_selectors, details)
    check_radio(driver, form_selectors, details)
    pick_option(driver, form_selectors, details)
    tick_checkboxes(driver, form_selectors, details)
    tick_captcha_checkbox(driver)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
