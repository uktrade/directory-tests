# -*- coding: utf-8 -*-
"""Domestic - Sort Domestic Contact us form"""
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
    tick_captcha_checkbox,
    tick_checkboxes,
)
from pages.domestic import contact_us_short_domestic_thank_you

NAME = "Short contact form (Tell us how we can help)"
NAMES = [
    "Short contact form (Tell us how we can help)",
    "Short contact form (Events)",
    "Short contact form (Defence and Security Organisation (DSO))",
    "Short contact form (Other)",
    "Short contact form (Office Finder)",
]
SERVICE = Service.DOMESTIC
TYPE = PageType.CONTACT_US
URL = URLs.CONTACT_US_FORM_DOMESTIC.absolute
PAGE_TITLE = "Welcome to great.gov.uk"

SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#lede form"),
        "comment": Selector(By.ID, "id_comment", type=ElementType.TEXTAREA),
        "first name": Selector(By.ID, "id_given_name", type=ElementType.INPUT),
        "last name": Selector(By.ID, "id_family_name", type=ElementType.INPUT),
        "email": Selector(By.ID, "id_email", type=ElementType.INPUT),
        "uk private or public limited company": Selector(
            By.CSS_SELECTOR, "input[value='LIMITED']", type=ElementType.RADIO
        ),
        "other type of uk organisation": Selector(
            By.CSS_SELECTOR, "input[value='OTHER']", type=ElementType.RADIO
        ),
        "organisation name": Selector(
            By.ID, "id_organisation_name", type=ElementType.INPUT
        ),
        "postcode": Selector(By.ID, "id_postcode", type=ElementType.INPUT),
        "terms": Selector(
            By.ID,
            "id_terms_agreed",
            type=ElementType.CHECKBOX,
            is_visible=False,
            alternative_visibility_check=True,
        ),
        "by email": Selector(
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
    "other": Selector(By.ID, "id_company_type_other", type=ElementType.SELECT)
}

SubURLs = {
    "short contact form (tell us how we can help)": URL,
    "short contact form (events)": URLs.CONTACT_US_FORM_EVENTS.absolute,
    "short contact form (defence and security organisation (dso))": URLs.CONTACT_US_FORM_DSO.absolute,
    "short contact form (other)": URLs.CONTACT_US_FORM_DOMESTIC_ENQUIRES.absolute,
    "short contact form (office finder)": URLs.CONTACT_US_OFFICE_FINDER.absolute,
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver, *, page_name: str = None):
    url = SubURLs[page_name.lower()] if page_name else URL
    check_url(driver, url, exact_match=True)


def generate_form_details(actor: Actor) -> dict:
    is_company = random.choice([True, False])
    by_email = random.choice([True, False])
    result = {
        "comment": f"Submitted by automated tests {actor.alias}",
        "first name": f"send by {actor.alias} - automated tests",
        "last name": str(uuid4()),
        "email": actor.email,
        "uk private or public limited company": is_company,
        "other type of uk organisation": not is_company,
        "organisation name": "automated tests",
        "postcode": "SW1H 0TL",
        "terms": True,
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
    fill_out_textarea_fields(driver, form_selectors, details)
    fill_out_input_fields(driver, form_selectors, details)
    check_radio(driver, form_selectors, details)
    tick_checkboxes(driver, form_selectors, details)
    pick_option(driver, form_selectors, details)
    tick_captcha_checkbox(driver)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
