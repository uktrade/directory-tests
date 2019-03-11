# -*- coding: utf-8 -*-
"""Profile - Enrol - Enter your business details"""
import logging
import random
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
)
from pages.profile import enrol_enter_your_business_details_step_2
from pages.profile.autocomplete_callbacks import enrol_autocomplete_company_name
from settings import DIRECTORY_UI_PROFILE_URL


NAME = "Enter your business details"
NAMES = ["Enter your business details (LTD, PLC or Royal Charter)"]
SERVICE = "Profile"
TYPE = "Enrol"
URL = urljoin(
    DIRECTORY_UI_PROFILE_URL, "enrol/business-type/companies-house/search/"
)
URLs = {
    "enter your business details (ltd, plc or royal charter)": urljoin(
        DIRECTORY_UI_PROFILE_URL, "enrol/business-type/companies-house/search/"
    )
}
PAGE_TITLE = ""

AUTOCOMPLETION = Selector(By.CSS_SELECTOR, "ul.SelectiveLookupDisplay")
AUTOCOMPLETION_OPTIONS = Selector(By.CSS_SELECTOR, "li[role='option']")
SELECTORS = {
    "enrolment progress bar": {"itself": Selector(By.ID, "progress-column")},
    "your business type": {
        "itself": Selector(By.ID, "business-type-information-box"),
        "business type": Selector(By.ID, "business-type"),
        "change business type": Selector(
            By.ID, "change-business-type", type=ElementType.LINK
        ),
    },
    "enter your business details": {
        "itself": Selector(By.CSS_SELECTOR, "section form"),
        "heading": Selector(By.CSS_SELECTOR, "#form-step-body-text h1"),
        "company name": Selector(
            By.ID,
            "id_search-company_name",
            type=ElementType.INPUT,
            is_visible=False,
            autocomplete_callback=enrol_autocomplete_company_name,
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
    words = [
        "food", "sell", "office", "work", "private", "trade", "fruits",
        "import", "cars", "animal", "limited", "group", "music", "open",
    ]
    result = {"company name": random.choice(words)}
    logging.debug(f"Generated form details: {result}")
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["enter your business details"]
    fill_out_input_fields(driver, form_selectors, details)
    take_screenshot(driver, "After filling out the form")


def submit(driver: WebDriver) -> ModuleType:
    take_screenshot(driver, "Before submitting the form")
    find_and_click_on_page_element(
        driver, SELECTORS, "submit", wait_for_it=False
    )
    take_screenshot(driver, "After submitting the form")
    return enrol_enter_your_business_details_step_2
