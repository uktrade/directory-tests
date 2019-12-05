# -*- coding: utf-8 -*-
"""Find a Supplier - Contact us."""
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
    check_url,
    fill_out_input_fields,
    fill_out_textarea_fields,
    go_to_url,
    pick_option,
    submit_form,
    take_screenshot,
    tick_captcha_checkbox,
    tick_checkboxes_by_labels,
)

NAME = "Find a UK business partner"
SERVICE = Service.INTERNATIONAL
TYPE = PageType.CONTACT_US
URL = URLs.FAS_CONTACT_US.absolute
PAGE_TITLE = "Contact us - trade.great.gov.uk"

SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#lede form"),
        "full name": Selector(By.ID, "id_full_name", type=ElementType.INPUT),
        "email": Selector(By.ID, "id_email_address", type=ElementType.INPUT),
        "phone number": Selector(By.ID, "id_phone_number", type=ElementType.INPUT),
        "industry": Selector(By.ID, "id_sector", type=ElementType.SELECT),
        "organisation": Selector(By.ID, "id_organisation_name", type=ElementType.INPUT),
        "organisation size": Selector(
            By.ID, "id_organisation_size", type=ElementType.SELECT
        ),
        "country": Selector(By.ID, "js-country-select", type=ElementType.SELECT),
        "body": Selector(By.ID, "id_body", type=ElementType.INPUT),
        "source": Selector(By.ID, "id_source", type=ElementType.SELECT),
        "accept t&c": Selector(
            By.ID, "id_terms_agreed", type=ElementType.LABEL, is_visible=False
        ),
        "submit": Selector(
            By.CSS_SELECTOR, "form input[type=submit]", type=ElementType.SUBMIT
        ),
    }
}
SELECTORS.update(common_selectors.INTERNATIONAL_HEADER_WO_LANGUAGE_SELECTOR)
SELECTORS.update(common_selectors.INTERNATIONAL_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=False)
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def generate_form_details(actor: Actor, *, custom_details: dict = None) -> dict:
    company_name = actor.company_name or "Automated test"
    result = {
        "full name": str(uuid4()),
        "email": actor.email,
        "phone number": "this is a test",
        "industry": None,
        "organisation": company_name,
        "organisation size": None,
        "country": None,
        "body": "This is a test message sent via automated tests",
        "source": None,
        "accept t&c": True,
        "captcha": True,
    }
    if custom_details:
        if custom_details.get("industry", None):
            custom_details["industry"] = (
                custom_details["industry"].lower().replace(" ", "-")
            )
        result.update(custom_details)
    return result


def fill_out(driver: WebDriver, contact_us_details: dict, *, captcha: bool = True):
    form_selectors = SELECTORS["form"]

    fill_out_input_fields(driver, form_selectors, contact_us_details)
    fill_out_textarea_fields(driver, form_selectors, contact_us_details)
    pick_option(driver, form_selectors, contact_us_details)
    tick_checkboxes_by_labels(driver, form_selectors, contact_us_details)

    if contact_us_details["captcha"]:
        tick_captcha_checkbox(driver)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
