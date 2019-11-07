# -*- coding: utf-8 -*-
"""Invest in Great - Contact us Page Object."""
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
    find_element,
    find_selector_by_name,
    pick_option,
    submit_form,
    take_screenshot,
    tick_captcha_checkbox,
    tick_checkboxes,
    visit_url,
)

NAME = "HPO Contact us"
NAMES = [
    "High productivity food production",
    "Lightweight structures",
    "Rail infrastructure",
]
SERVICE = Service.INVEST
TYPE = PageType.CONTACT_US
URL = URLs.INVEST_HPO_CONTACT.absolute
SubURLs = {
    "high productivity food production": URL,
    "lightweight structures": URL,
    "rail infrastructure": URL,
}
PAGE_TITLE = ""

IM_NOT_A_ROBOT = Selector(By.CSS_SELECTOR, ".recaptcha-checkbox-checkmark")
SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#content form"),
        "full name": Selector(By.ID, "id_full_name", type=ElementType.INPUT),
        "job title": Selector(By.ID, "id_role_in_company", type=ElementType.INPUT),
        "email": Selector(By.ID, "id_email_address", type=ElementType.INPUT),
        "phone": Selector(By.ID, "id_phone_number", type=ElementType.INPUT),
        "company name": Selector(By.ID, "id_company_name", type=ElementType.INPUT),
        "website url": Selector(By.ID, "id_website_url", type=ElementType.INPUT),
        "country": Selector(
            By.ID, "js-country-select-select", type=ElementType.SELECT, is_visible=False
        ),
        "organisation size": Selector(
            By.ID, "id_company_size", type=ElementType.SELECT
        ),
        "aquaculture": Selector(
            By.ID,
            "checkbox-multiple-aquaculture",
            type=ElementType.CHECKBOX,
            is_visible=False,
            alternative_visibility_check=True,
        ),
        "advanced food production": Selector(
            By.ID,
            "checkbox-multiple-high-productivity-food-production",
            type=ElementType.CHECKBOX,
            is_visible=False,
            alternative_visibility_check=True,
        ),
        "rail infrastructure": Selector(
            By.ID,
            "checkbox-multiple-rail-infrastructure",
            type=ElementType.CHECKBOX,
            is_visible=False,
            alternative_visibility_check=True,
        ),
        "lightweight structures": Selector(
            By.ID,
            "checkbox-multiple-lightweight-structures",
            type=ElementType.CHECKBOX,
            is_visible=False,
            alternative_visibility_check=True,
        ),
        "photonics and microelectronics": Selector(
            By.ID,
            "checkbox-multiple-photonics-and-microelectronics",
            type=ElementType.CHECKBOX,
            is_visible=False,
            alternative_visibility_check=True,
        ),
        "space": Selector(
            By.ID,
            "checkbox-multiple-space",
            type=ElementType.CHECKBOX,
            is_visible=False,
            alternative_visibility_check=True,
        ),
        "sustainable packaging": Selector(
            By.ID,
            "checkbox-multiple-sustainable-packaging",
            type=ElementType.CHECKBOX,
            is_visible=False,
            alternative_visibility_check=True,
        ),
        "terms and conditions": Selector(
            By.ID,
            "id_terms_agreed",
            type=ElementType.CHECKBOX,
            is_visible=False,
            alternative_visibility_check=True,
        ),
        "comment": Selector(By.ID, "id_comment", type=ElementType.TEXTAREA),
        "terms and conditions link": Selector(
            By.CSS_SELECTOR, "#id_terms_agreed-label a"
        ),
        "captcha": Selector(
            By.CSS_SELECTOR, "#form-container iframe", type=ElementType.IFRAME
        ),
        "submit": Selector(By.ID, "submit-button", type=ElementType.SUBMIT),
    },
    "elements invisible to selenium": {},
}
SELECTORS.update(common_selectors.INVEST_HEADER)
SELECTORS.update(common_selectors.BETA_BAR)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.INVEST_FOOTER)


def visit(driver: WebDriver, *, page_name: str = None):
    url = SubURLs[page_name] if page_name else URL
    visit_url(driver, url)


def should_be_here(driver: WebDriver, *, page_name: str):
    take_screenshot(driver, PAGE_TITLE)
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def check_state_of_form_element(
    driver: WebDriver, element_name: str, expected_state: str
):
    element_selector = find_selector_by_name(SELECTORS, element_name)
    element = find_element(driver, element_selector, wait_for_it=False)
    if expected_state == "selected":
        assert element.get_property("checked")


def generate_form_details(actor: Actor, *, custom_details: dict = None) -> dict:
    details = {
        "full name": str(uuid4()),
        "job title": "QA @ DIT",
        "email": actor.email,
        "phone": "0123456789",
        "company name": actor.company_name or "Automated test - company name",
        "website url": "https://browser.tests.com",
        "country": None,
        "organisation size": None,
        "comment": "This form was submitted by Automated test",
        "aquaculture": True,
        "advanced food production": True,
        "lightweight structures": True,
        "rail infrastructure": True,
        "photonics and microelectronics": True,
        "space": True,
        "sustainable packaging": True,
        "terms and conditions": True,
    }
    if custom_details:
        details.update(custom_details)
    logging.debug(f"Form details: {details}")
    return details


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    fill_out_input_fields(driver, form_selectors, details)
    fill_out_textarea_fields(driver, form_selectors, details)
    pick_option(driver, form_selectors, details)
    tick_checkboxes(driver, form_selectors, details)
    tick_captcha_checkbox(driver)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
