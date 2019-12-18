# -*- coding: utf-8 -*-
"""Find a Supplier Search Results Page Object."""
import logging
from types import ModuleType
from typing import List, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType, common_selectors
from pages.common_actions import (
    Actor,
    Selector,
    check_for_sections,
    check_url,
    fill_out_input_fields,
    go_to_url,
    pick_option,
    submit_form,
    tick_captcha_checkbox,
    tick_checkboxes,
)
from pages.fas import thank_you_for_registering

NAME = "Subscribe for email updates"
SERVICE = Service.FAS
TYPE = PageType.FORM
URL = URLs.FAS_SUBSCRIBE.absolute
PAGE_TITLE = "great.gov.uk international"

SELECTORS = {
    "subscribe for email updates": {
        "full name": Selector(By.ID, "id_full_name", type=ElementType.INPUT),
        "email": Selector(By.ID, "id_email_address", type=ElementType.INPUT),
        "industry": Selector(By.ID, "id_sector", type=ElementType.SELECT),
        "company name": Selector(By.ID, "id_company_name", type=ElementType.INPUT),
        "country": Selector(By.ID, "id_country", type=ElementType.SELECT),
        "t&c": Selector(By.ID, "id_terms", type=ElementType.CHECKBOX),
        "captcha": Selector(By.ID, "id_captcha"),
        "send": Selector(
            By.CSS_SELECTOR,
            "#id_terms-container ~ button",
            type=ElementType.SUBMIT,
            next_page=thank_you_for_registering,
        ),
    }
}
SELECTORS.update(common_selectors.INTERNATIONAL_HEADER_WO_LANGUAGE_SELECTOR)
SELECTORS.update(common_selectors.INTERNATIONAL_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def generate_form_details(actor: Actor, *, custom_details: dict = None) -> dict:
    result = {
        "full name": actor.alias,
        "email": actor.email,
        "industry": None,
        "company name": "AUTOMATED TESTS",
        "country": None,
        "t&c": True,
    }
    if custom_details:
        result.update(custom_details)
    return result


def fill_out(driver: WebDriver, contact_us_details: dict):
    form_selectors = SELECTORS["subscribe for email updates"]
    fill_out_input_fields(driver, form_selectors, contact_us_details)
    pick_option(driver, form_selectors, contact_us_details)
    tick_checkboxes(driver, form_selectors, contact_us_details)
    tick_captcha_checkbox(driver)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["subscribe for email updates"])
