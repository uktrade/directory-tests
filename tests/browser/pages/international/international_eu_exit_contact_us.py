# -*- coding: utf-8 -*-
"""International - EU Exit Contact us page"""
import random
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
    check_if_element_is_not_visible,
    check_url,
    fill_out_input_fields,
    fill_out_textarea_fields,
    go_to_url,
    pick_option,
    submit_form,
    tick_captcha_checkbox,
    tick_checkboxes,
)

NAME = "Brexit help"
SERVICE = Service.INTERNATIONAL
TYPE = PageType.CONTACT_US
URL = URLs.CONTACT_US_INTERNATIONAL_BREXIT_CONTACT.absolute
PAGE_TITLE = "Welcome to great.gov.uk - buy from or invest in the UK"

SELECTORS = {
    "heading": {
        "itself": Selector(By.CSS_SELECTOR, "#content h1"),
        "text": Selector(By.CSS_SELECTOR, "#content p.body-text"),
    },
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#content form"),
        "given names": Selector(By.ID, "id_first_name", type=ElementType.INPUT),
        "family name": Selector(By.ID, "id_last_name", type=ElementType.INPUT),
        "email": Selector(By.ID, "id_email", type=ElementType.INPUT),
        "company": Selector(
            By.ID, "id_organisation_type_0", type=ElementType.CHECKBOX, is_visible=False
        ),
        "other type of organisation": Selector(
            By.ID, "id_organisation_type_0", type=ElementType.CHECKBOX, is_visible=False
        ),
        "company name": Selector(By.ID, "id_company_name", type=ElementType.INPUT),
        "country": Selector(By.ID, "js-country-select", type=ElementType.SELECT),
        "city": Selector(By.ID, "id_city", type=ElementType.INPUT),
        "comment": Selector(By.ID, "id_comment", type=ElementType.TEXTAREA),
        "terms and conditions": Selector(
            By.ID, "id_terms_agreed", type=ElementType.CHECKBOX, is_visible=False
        ),
        "submit": Selector(
            By.CSS_SELECTOR, "form[method=POST] button", type=ElementType.SUBMIT
        ),
    },
    "error reporting": {
        "itself": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "link": Selector(By.ID, "error-reporting-section-contact-us"),
    },
}
SELECTORS.update(common_selectors.INTERNATIONAL_HEADER_WO_LANGUAGE_SELECTOR)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.INTERNATIONAL_FOOTER)

UNEXPECTED_SELECTORS = {
    "not translated": {
        "not translated": Selector(By.ID, "header-label-not-translated")
    },
    "language selector": {
        "language selector": Selector(
            By.CSS_SELECTOR,
            "#international-header-bar .LanguageSelectorDialog-Tracker",
            is_visible=False,
        )
    },
}

ALL_SELECTORS = {}
ALL_SELECTORS.update(SELECTORS)
ALL_SELECTORS.update(UNEXPECTED_SELECTORS)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=False)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=ALL_SELECTORS, sought_sections=names)


def should_not_see_section(driver: WebDriver, name: str):
    section = UNEXPECTED_SELECTORS[name.lower()]
    for key, selector in section.items():
        check_if_element_is_not_visible(driver, selector, element_name=key)


def generate_form_details(actor: Actor) -> dict:
    is_company = random.choice([True, False])
    result = {
        "given names": f"send by {actor.alias} - automated tests",
        "family name": str(uuid4()),
        "email": actor.email,
        "company": is_company,
        "other type of organisation": not is_company,
        "company name": "automated tests",
        "country": None,
        "city": "automated tests",
        "comment": f"Submitted by automated tests {actor.alias}",
        "terms and conditions": True,
    }
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    fill_out_input_fields(driver, form_selectors, details)
    fill_out_textarea_fields(driver, form_selectors, details)
    pick_option(driver, form_selectors, details)
    tick_checkboxes(driver, form_selectors, details)
    tick_captcha_checkbox(driver)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
