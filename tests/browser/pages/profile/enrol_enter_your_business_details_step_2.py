# -*- coding: utf-8 -*-
"""Profile - Enrol - Enter your business details"""
import logging
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
    find_elements_of_type,
    go_to_url,
    pick_option,
    submit_form,
    take_screenshot,
)
from pages.profile import enrol_enter_your_details

NAME = "Enter your business details [step 2]"
NAMES = ["Enter your business details [step 2] (LTD, PLC or Royal Charter)"]
SERVICE = Service.PROFILE
TYPE = PageType.FORM
URL = URLs.PROFILE_ENROL_BUSINESS_DETAILS.absolute
SubURLs = {"enter your business details [step 2] (ltd, plc or royal charter)": URL}
PAGE_TITLE = ""

INDUSTRY = Selector(
    By.ID, "id_business-details-sectors", is_visible=False, type=ElementType.SELECT
)
WEBSITE = Selector(
    By.ID, "id_business-details-website", is_visible=False, type=ElementType.INPUT
)
SELECTORS = {
    "enrolment progress bar": {"itself": Selector(By.ID, "progress-column")},
    "enter your business details": {
        "itself": Selector(By.CSS_SELECTOR, "section form"),
        "heading": Selector(By.CSS_SELECTOR, "h2"),
        "text": Selector(By.ID, "form-step-body-text"),
        "company name": Selector(By.ID, "id_business-details-company_name"),
        "industry": INDUSTRY,
        "website": WEBSITE,
        "submit": Selector(
            By.CSS_SELECTOR,
            "form button.button",
            type=ElementType.SUBMIT,
            next_page=enrol_enter_your_details,
        ),
    },
}
FORM_FIELDS_WITH_USEFUL_DATA = {
    "company name": Selector(
        By.ID, "id_business-details-company_name", type=ElementType.INPUT
    ),
    "company number": Selector(
        By.ID,
        "id_business-details-company_number",
        type=ElementType.INPUT,
        is_visible=False,
    ),
    "industry": INDUSTRY,
    "company website": WEBSITE,
    "sic": Selector(By.ID, "id_business-details-sic", type=ElementType.INPUT),
    "date_of_creation": Selector(
        By.ID, "id_business-details-date_of_creation", type=ElementType.INPUT
    ),
    "address": Selector(By.ID, "id_business-details-address", type=ElementType.INPUT),
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver, *, page_name: str = None):
    take_screenshot(driver, NAME)
    url = SubURLs[page_name.lower()] if page_name else URL
    check_url(driver, url, exact_match=False)
    msg = f"Got 404 on {driver.current_url}"
    assert "This page cannot be found" not in driver.page_source, msg


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def generate_form_details(actor: Actor) -> dict:
    result = {"industry": None, "website": "https://automated.test.com"}
    logging.debug(f"Generated form details: {result}")
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["enter your business details"]
    pick_option(driver, form_selectors, details)
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
        text = element.get_attribute("text")
        result[key] = value or text

    return dict(result)
