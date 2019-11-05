# -*- coding: utf-8 -*-
"""Profile - Enrol - Enter your business details"""
import logging
import random
from collections import defaultdict
from types import ModuleType
from typing import List, Union

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
    find_and_click_on_page_element,
    find_elements_of_type,
    go_to_url,
    submit_form,
    take_screenshot,
)
from pages.profile import enrol_enter_your_business_details_step_2
from pages.profile.autocomplete_callbacks import enrol_autocomplete_company_name

NAME = "Enter your business details (LTD, PLC or Royal Charter)"
SERVICE = Service.PROFILE
TYPE = PageType.FORM
URL = URLs.PROFILE_ENROL_COMPANIES_HOUSE_SEARCH.absolute
PAGE_TITLE = ""

SELECTORS = {
    "enrolment progress bar": {"itself": Selector(By.ID, "progress-column")},
    "your business type": {
        "information box": Selector(By.ID, "business-type-information-box"),
        "change business type": Selector(By.ID, "change-business-type"),
    },
    "enter your business details": {
        "itself": Selector(By.CSS_SELECTOR, "section form"),
        "heading": Selector(By.CSS_SELECTOR, "#form-step-body-text h1"),
        "company name": Selector(
            By.ID,
            "id_company-search-company_name",
            type=ElementType.INPUT,
            is_visible=False,
            autocomplete_callback=enrol_autocomplete_company_name,
        ),
        "i cannot find my business name": Selector(
            By.CSS_SELECTOR,
            "details summary",
            type=ElementType.LINK,
            wait_after_click=False,
        ),
        "contact us": Selector(
            By.CSS_SELECTOR, "details a", type=ElementType.LINK, is_visible=False
        ),
        "submit": Selector(
            By.CSS_SELECTOR,
            "form button.button",
            type=ElementType.SUBMIT,
            next_page=enrol_enter_your_business_details_step_2,
        ),
    },
}
FORM_FIELDS_WITH_USEFUL_DATA = {
    "company name": Selector(
        By.ID, "id_company-search-company_name", type=ElementType.INPUT
    ),
    "company number": Selector(
        By.ID,
        "id_company-search-company_number",
        type=ElementType.INPUT,
        is_visible=False,
    ),
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    msg = f"Got 404 on {driver.current_url}"
    assert "This page cannot be found" not in driver.page_source, msg


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def generate_form_details(actor: Actor) -> dict:
    words = [
        "food",
        "sell",
        "office",
        "work",
        "private",
        "trade",
        "fruits",
        "import",
        "cars",
        "animal",
        "limited",
        "group",
        "music",
        "open",
    ]
    result = {"company name": random.choice(words)}
    logging.debug(f"Generated form details: {result}")
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["enter your business details"]
    fill_out_input_fields(driver, form_selectors, details)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["enter your business details"])


def get_form_details(driver: WebDriver) -> dict:
    elements = find_elements_of_type(
        driver, FORM_FIELDS_WITH_USEFUL_DATA, ElementType.INPUT
    )
    result = defaultdict()
    for key, element in elements.items():
        value = element.get_attribute("value")
        result[key] = value

    return dict(result)


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
