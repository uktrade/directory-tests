# -*- coding: utf-8 -*-
"""PIR - Landing Page"""
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
    go_to_url,
    pick_option,
    submit_form,
    tick_captcha_checkbox,
    tick_checkboxes,
)

NAME = "Landing"
SERVICE = Service.PIR
TYPE = PageType.LANDING
URL = URLs.INVEST_PIR.absolute

SELECTORS = {
    "hero": {
        "self": Selector(By.ID, "hero"),
        "heading": Selector(By.CSS_SELECTOR, "#hero h1"),
    },
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#content form"),
        "name": Selector(By.ID, "id_name", type=ElementType.INPUT),
        "company": Selector(By.ID, "id_company", type=ElementType.INPUT),
        "email": Selector(By.ID, "id_email", type=ElementType.INPUT),
        "phone": Selector(By.ID, "id_phone_number", type=ElementType.INPUT),
        "country": Selector(By.ID, "id_country", type=ElementType.SELECT),
        "sector": Selector(By.ID, "id_sector", type=ElementType.SELECT),
        "send updates": Selector(
            By.ID, "id_gdpr_optin", type=ElementType.CHECKBOX, is_visible=False
        ),
        "submit": Selector(
            By.CSS_SELECTOR, "form input.button[type=submit]", type=ElementType.SUBMIT
        ),
    },
}
SELECTORS.update(common_selectors.INTERNATIONAL_HEADER_WO_LANGUAGE_SELECTOR)
SELECTORS.update(common_selectors.INTERNATIONAL_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def generate_form_details(actor: Actor, *, custom_details: dict = None) -> dict:
    details = {
        "name": str(uuid4()),
        "company": actor.company_name or "Automated test - company name",
        "email": actor.email,
        "phone": "0123456789",
        "country": None,
        "sector": None,
        "send updates": True,
    }
    if custom_details:
        details.update(custom_details)
    return details


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    fill_out_input_fields(driver, form_selectors, details)
    pick_option(driver, form_selectors, details)
    tick_checkboxes(driver, form_selectors, details)
    tick_captcha_checkbox(driver)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
