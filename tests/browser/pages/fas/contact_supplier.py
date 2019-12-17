# -*- coding: utf-8 -*-
"""Find a Supplier Landing Page Object."""
import logging
from types import ModuleType
from typing import List, Union
from uuid import uuid4

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType, common_selectors
from pages.common_actions import (
    Actor,
    Selector,
    check_for_sections,
    fill_out_input_fields,
    fill_out_textarea_fields,
    go_to_url,
    pick_option,
    submit_form,
    tick_captcha_checkbox,
    tick_checkboxes,
)

NAME = "Contact Supplier"
SERVICE = Service.FAS
TYPE = PageType.CONTACT_US
URL = URLs.FAS_CONTACT_SUPPLIER.absolute_template
PAGE_TITLE = "Find a Buyer - GREAT.gov.uk"

SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#content form"),
        "given name": Selector(By.ID, "id_given_name", type=ElementType.INPUT),
        "family name": Selector(By.ID, "id_family_name", type=ElementType.INPUT),
        "company name": Selector(By.ID, "id_company_name", type=ElementType.INPUT),
        "country": Selector(By.ID, "id_country", type=ElementType.INPUT),
        "email": Selector(By.ID, "id_email_address", type=ElementType.INPUT),
        "industry": Selector(By.ID, "id_sector", type=ElementType.SELECT),
        "subject": Selector(By.ID, "id_subject", type=ElementType.INPUT),
        "message": Selector(By.ID, "id_body", type=ElementType.TEXTAREA),
        "t&c": Selector(By.ID, "id_terms", type=ElementType.CHECKBOX, is_visible=False),
        "send": Selector(
            By.CSS_SELECTOR, "#content form button.button", type=ElementType.SUBMIT
        ),
    }
}
SELECTORS.update(common_selectors.INTERNATIONAL_HEADER_WO_LANGUAGE_SELECTOR)
SELECTORS.update(common_selectors.INTERNATIONAL_FOOTER)


def visit(driver: WebDriver, company_number: str):
    url = URL.format(ch_number=company_number)
    go_to_url(driver, url, NAME)


def should_be_here(driver: WebDriver):
    should_see_sections(driver, ["form"])
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def generate_form_details(actor: Actor, *, custom_details: dict = None) -> dict:
    company_name = actor.company_name or "Automated test"
    result = {
        "given name": actor.alias,
        "family name": str(uuid4()),
        "company name": company_name,
        "country": "AUTOMATED TESTS",
        "email": actor.email,
        "industry": None,
        "subject": "AUTOMATED TESTS",
        "message": "This is a test message sent via automated tests",
        "t&c": True,
    }
    if custom_details:
        result.update(custom_details)
    return result


def fill_out(driver: WebDriver, contact_us_details: dict, *, captcha: bool = True):
    form_selectors = SELECTORS["form"]

    fill_out_input_fields(driver, form_selectors, contact_us_details)
    pick_option(driver, form_selectors, contact_us_details)
    fill_out_textarea_fields(driver, form_selectors, contact_us_details)
    tick_checkboxes(driver, form_selectors, contact_us_details)

    if captcha:
        tick_captcha_checkbox(driver)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
