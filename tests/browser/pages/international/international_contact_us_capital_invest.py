# -*- coding: utf-8 -*-
"""International - Contact the Capital Investment team page"""
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
    tick_checkboxes,
)
from pages.international import international_contact_us_capital_invest_thank_you

NAME = "Contact the Capital Investment team"
SERVICE = Service.INTERNATIONAL
TYPE = PageType.CONTACT_US
URL = URLs.INTERNATIONAL_CAPITAL_INVEST_CONTACT.absolute
PAGE_TITLE = "Capital Invest Contact Form - great.gov.uk international"

SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#content form"),
        "given name": Selector(By.ID, "id_given_name", type=ElementType.INPUT),
        "family name": Selector(By.ID, "id_family_name", type=ElementType.INPUT),
        "email": Selector(By.ID, "id_email_address", type=ElementType.INPUT),
        "phone number": Selector(By.ID, "id_phone_number", type=ElementType.INPUT),
        "country": Selector(By.ID, "js-country-select", type=ElementType.SELECT),
        "city": Selector(By.ID, "id_city", type=ElementType.INPUT),
        "company name": Selector(By.ID, "id_company_name", type=ElementType.INPUT),
        "message": Selector(By.ID, "id_message", type=ElementType.TEXTAREA),
        "terms and conditions": Selector(
            By.ID, "id_terms_agreed", type=ElementType.CHECKBOX, is_visible=False
        ),
        "submit": Selector(
            By.CSS_SELECTOR,
            "form[method=POST] button",
            type=ElementType.SUBMIT,
            next_page=international_contact_us_capital_invest_thank_you,
        ),
    }
}

SELECTORS.update(common_selectors.INTERNATIONAL_HEADER)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.INTERNATIONAL_FOOTER)


def visit(driver: WebDriver, *, page_name: str = None):
    go_to_url(driver, URL, page_name or NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def generate_form_details(actor: Actor) -> dict:
    result = {
        "given name": f"send by {actor.alias} - automated tests",
        "family name": str(uuid4()),
        "email": actor.email,
        "phone number": "01234567890",
        "country": None,
        "city": "automated tests",
        "company name": "automated tests",
        "message": f"Submitted by automated tests {actor.alias}",
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
