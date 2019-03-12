# -*- coding: utf-8 -*-
"""Profile - Enrol - Enter your details"""
import logging
from types import ModuleType
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Actor,
    Selector,
    check_for_sections,
    check_url,
    fill_out_input_fields,
    find_and_click_on_page_element,
    go_to_url,
    take_screenshot,
    tick_checkboxes,
)
from pages.profile import enrol_account_created
from settings import DIRECTORY_UI_PROFILE_URL

NAME = "Enter your details"
NAMES = ["Enter your details (LTD, PLC or Royal Charter)"]
SERVICE = "Profile"
TYPE = "Enrol"
URL = urljoin(
    DIRECTORY_UI_PROFILE_URL,
    "enrol/business-type/companies-house/personal-details/",
)
URLs = {"enter your details (ltd, plc or royal charter)": URL}
PAGE_TITLE = ""

SELECTORS = {
    "enrolment progress bar": {"itself": Selector(By.ID, "progress-column")},
    "your business details": {
        "itself": Selector(By.ID, "business-details-information-box"),
        "company name": Selector(By.ID, "company-name"),
        "company address": Selector(By.ID, "company-address"),
        "change business details": Selector(
            By.ID, "change-business-details", type=ElementType.LINK
        ),
    },
    "enter your details form": {
        "itself": Selector(By.CSS_SELECTOR, "section form"),
        "heading": Selector(By.CSS_SELECTOR, "h1"),
        "first name": Selector(
            By.ID, "id_personal-details-given_name", type=ElementType.INPUT
        ),
        "last name": Selector(
            By.ID, "id_personal-details-family_name", type=ElementType.INPUT
        ),
        "job title": Selector(
            By.ID, "id_personal-details-job_title", type=ElementType.INPUT
        ),
        "phone number": Selector(
            By.ID, "id_personal-details-phone_number", type=ElementType.INPUT
        ),
        "background checks": Selector(
            By.ID,
            "id_personal-details-confirmed_is_company_representative",
            type=ElementType.CHECKBOX,
            is_visible=False,
        ),
        "list of background checks": Selector(
            By.ID, "list-background-checks", type=ElementType.LINK
        ),
        "submit": Selector(
            By.CSS_SELECTOR, "form button.button", type=ElementType.BUTTON
        ),
    },
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver, *, page_name: str = None):
    take_screenshot(driver, NAME)
    url = URLs[page_name.lower()] if page_name else URL
    check_url(driver, url, exact_match=False)
    msg = f"Got 404 on {driver.current_url}"
    assert "This page cannot be found" not in driver.page_source, msg


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def generate_form_details(actor: Actor) -> dict:
    result = {
        "first name": actor.alias,
        "last name": "automated tests",
        "job title": "automated tests",
        "phone number": "07123456789",
        "background checks": True,
    }
    logging.debug(f"Generated form details: {result}")
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["enter your details form"]
    fill_out_input_fields(driver, form_selectors, details)
    tick_checkboxes(driver, form_selectors, details)
    take_screenshot(driver, "After filling out the form")


def submit(driver: WebDriver) -> ModuleType:
    take_screenshot(driver, "Before submitting the form")
    find_and_click_on_page_element(
        driver, SELECTORS, "submit", wait_for_it=False
    )
    take_screenshot(driver, "After submitting the form")
    return enrol_account_created
