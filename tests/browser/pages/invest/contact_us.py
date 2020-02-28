# -*- coding: utf-8 -*-
"""Invest in Great - Contact us Page Object."""
import logging
from random import choice
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
    check_radio,
    check_url,
    fill_out_input_fields,
    fill_out_textarea_fields,
    go_to_url,
    pick_option,
    submit_form,
    tick_captcha_checkbox,
)
from pages.common_autocomplete_callbacks import js_country_select
from pages.invest import contact_us_thank_you

NAME = "Contact us"
SERVICE = Service.INVEST
TYPE = PageType.CONTACT_US
URL = URLs.INVEST_CONTACT.absolute
PAGE_TITLE = ""

SELECTORS = {
    "hero": {
        "itself": Selector(By.CSS_SELECTOR, "section.hero"),
        "heading": Selector(By.CSS_SELECTOR, "section.hero h1"),
    },
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#content form"),
        "given name": Selector(By.ID, "id_given_name", type=ElementType.INPUT),
        "family name": Selector(By.ID, "id_family_name", type=ElementType.INPUT),
        "job title": Selector(By.ID, "id_job_title", type=ElementType.INPUT),
        "email": Selector(By.ID, "id_email", type=ElementType.INPUT),
        "phone": Selector(By.ID, "id_phone_number", type=ElementType.INPUT),
        "company name": Selector(By.ID, "id_company_name", type=ElementType.INPUT),
        "website url": Selector(By.ID, "id_company_website", type=ElementType.INPUT),
        "company hq address": Selector(
            By.ID, "id_company_hq_address", type=ElementType.INPUT
        ),
        "country": Selector(
            By.CSS_SELECTOR,
            "form[method=post] #js-country-select-select",
            type=ElementType.INPUT,
            is_visible=False,
            autocomplete_callback=js_country_select,
        ),
        "industry": Selector(
            By.ID, "id_industry", type=ElementType.SELECT, is_visible=False
        ),
        "feeling": Selector(
            By.ID, "id_expanding_to_uk", type=ElementType.SELECT, is_visible=False
        ),
        "your plans": Selector(By.ID, "id_description", type=ElementType.TEXTAREA),
        "arrange call yes": Selector(
            By.ID, "id_arrange_callback_0", type=ElementType.RADIO
        ),
        "arrange call no": Selector(
            By.ID, "id_arrange_callback_1", type=ElementType.RADIO
        ),
        "how did you hear": Selector(
            By.ID, "id_how_did_you_hear", type=ElementType.SELECT, is_visible=False
        ),
        "updates by email": Selector(
            By.ID, "id_email_contact_consent", type=ElementType.CHECKBOX
        ),
        "updates by tel": Selector(
            By.ID, "id_telephone_contact_consent", type=ElementType.CHECKBOX
        ),
        "submit": Selector(
            By.CSS_SELECTOR,
            "#content form button.button",
            type=ElementType.SUBMIT,
            next_page=contact_us_thank_you,
        ),
    },
}
SELECTORS.update(common_selectors.INTERNATIONAL_HEADER)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.INVEST_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def generate_form_details(actor: Actor, *, custom_details: dict = None) -> dict:
    arrange_call = choice([True, False])
    details = {
        "given name": actor.company_name or "Automated test",
        "family name": actor.company_name or "Automated test",
        "job title": "QA @ DIT",
        "email": actor.email,
        "phone": "0123456789",
        "company name": actor.company_name or "Automated test - company name",
        "website url": "https://example.com",
        "company hq address": "Far, far away",
        "country": True,
        "industry": None,
        "feeling": None,
        "your plans": "This is a test message sent via automated tests",
        "arrange call yes": arrange_call,
        "arrange call no": not arrange_call,
        "how did you hear": None,
        "updates by email": choice([True, False]),
        "updates by tel": choice([True, False]),
    }

    if custom_details:
        details.update(custom_details)
    logging.debug(f"Generated form details: {details}")
    return details


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    fill_out_input_fields(driver, form_selectors, details)
    pick_option(driver, form_selectors, details)
    check_radio(driver, form_selectors, details)
    fill_out_textarea_fields(driver, form_selectors, details)
    tick_captcha_checkbox(driver)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
