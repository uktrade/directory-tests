# -*- coding: utf-8 -*-
"""great.gov.uk Domestic EU Exit Contact us page"""
import random
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Selector,
    check_url,
    find_element,
    go_to_url,
    take_screenshot,
    check_for_sections,
    AssertionExecutor,
    Actor,
    fill_out_textarea_fields,
    tick_checkboxes,
    tick_captcha_checkbox,
    fill_out_input_fields,
    pick_option,
)
from settings import EXRED_UI_URL

NAME = "Domestic EU Exit contact form"
SERVICE = "Export Readiness"
TYPE = "Contact us"
URL = urljoin(EXRED_UI_URL, "eu-exit/contact/")
PAGE_TITLE = ""


SUBMIT_BUTTON = Selector(By.CSS_SELECTOR, "form button")
SELECTORS = {
    "header bar": {
        "itself": Selector(By.ID, "header-bar"),
    },
    "header menu": {
        "itself": Selector(By.ID, "header-menu"),
        "logo": Selector(By.ID, "header-logo"),
        "breadcrumbs": Selector(By.CSS_SELECTOR, ".breadcrumbs"),
    },
    "heading": {
        "itself": Selector(By.CSS_SELECTOR, "#content h1"),
        "text": Selector(By.CSS_SELECTOR, "#content p.body-text")
    },
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#content form"),
        "fist name": Selector(By.ID, "id_first_name", type=ElementType.INPUT),
        "last name": Selector(By.ID, "id_last_name", type=ElementType.INPUT),
        "email": Selector(By.ID, "id_email", type=ElementType.INPUT),
        "company": Selector(By.ID, "id_organisation_type_0", type=ElementType.CHECKBOX, is_visible=False),
        "other type of organisation": Selector(By.ID, "id_organisation_type_0", type=ElementType.CHECKBOX, is_visible=False),
        "company name": Selector(By.ID, "id_company_name", type=ElementType.INPUT),
        "your question": Selector(By.ID, "id_comment", type=ElementType.TEXTAREA),
        "terms and conditions": Selector(
            By.ID,
            "id_terms_agreed",
            type=ElementType.CHECKBOX,
            is_visible=False,
        ),
        "submit": SUBMIT_BUTTON,
    },
    "error reporting": {
        "itself": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "link": Selector(By.ID, "error-reporting-section-contact-us"),
    },
}


def visit(driver: WebDriver, *, page_name: str = None, first_time: bool = False):
    go_to_url(driver, URL, page_name, first_time=first_time)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)


def should_see_sections(executor: AssertionExecutor, names: List[str]):
    check_for_sections(executor, all_sections=ALL_SELECTORS, sought_sections=names)


def generate_form_details(actor: Actor) -> dict:
    is_company = random.choice([True, False])
    result = {
        "first name": f"send by {actor.alias} - automated tests",
        "last name": actor.alias,
        "email": actor.email,
        "company": is_company,
        "other type of organisation": not is_company,
        "company name": "automated tests",
        "your question": f"Submitted by automated test {actor.alias}",
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
    take_screenshot(driver, "After filling out the form")


def submit(driver: WebDriver):
    take_screenshot(driver, "Before submitting the form")
    button = find_element(
        driver, SUBMIT_BUTTON, element_name="Submit button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, "After submitting the form")