# -*- coding: utf-8 -*-
"""great.gov.uk Domestic EU Exit Contact us page"""
import random
from types import ModuleType
from typing import List, Union
from uuid import uuid4

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType
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
    tick_captcha_checkbox,
    tick_checkboxes,
)

NAME = "Brexit help"
SERVICE = Service.DOMESTIC
TYPE = PageType.CONTACT_US
URL = URLs.CONTACT_US_DOMESTIC_BREXIT_CONTACT.absolute
PAGE_TITLE = ""

SELECTORS = {
    "header bar": {"itself": Selector(By.ID, "header-bar")},
    "header menu": {
        "itself": Selector(By.ID, "header-menu"),
        "logo": Selector(By.ID, "header-logo"),
        "breadcrumbs": Selector(By.CSS_SELECTOR, ".breadcrumbs"),
    },
    "heading": {
        "itself": Selector(By.CSS_SELECTOR, "#content h1"),
        "text": Selector(By.CSS_SELECTOR, "#content p.body-text"),
    },
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#content form"),
        "first name": Selector(By.ID, "id_first_name", type=ElementType.INPUT),
        "last name": Selector(By.ID, "id_last_name", type=ElementType.INPUT),
        "email": Selector(By.ID, "id_email", type=ElementType.INPUT),
        "company": Selector(
            By.CSS_SELECTOR,
            "input[value='COMPANY']",
            type=ElementType.CHECKBOX,
            is_visible=False,
        ),
        "other type of organisation": Selector(
            By.CSS_SELECTOR,
            "input[value='OTHER']",
            type=ElementType.CHECKBOX,
            is_visible=False,
        ),
        "company name": Selector(By.ID, "id_company_name", type=ElementType.INPUT),
        "your question": Selector(By.ID, "id_comment", type=ElementType.TEXTAREA),
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


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=False)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def generate_form_details(actor: Actor) -> dict:
    is_company = random.choice([True, False])
    result = {
        "first name": f"send by {actor.alias} - automated tests",
        "last name": str(uuid4()),
        "email": actor.email,
        "company": is_company,
        "other type of organisation": not is_company,
        "company name": "automated tests",
        "your question": f"Submitted by automated tests {actor.alias}",
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
