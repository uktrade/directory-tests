# -*- coding: utf-8 -*-
"""Profile - Enrol - Enter your business email address and set a password"""
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
    tick_captcha_checkbox,
    tick_checkboxes,
)
from pages.profile import enrol_enter_your_confirmation_code
from settings import DIRECTORY_UI_PROFILE_URL

NAME = "Enter your business email address and set a password"
NAMES = [
    "Enter your business email address and set a password",
    "Enter your business email address and set a password (LTD, PLC or Royal Charter)",
    "Enter your business email address and set a password (Sole trader or other type of business)",
]
SERVICE = "Profile"
TYPE = "Enrol"
URL = urljoin(
    DIRECTORY_UI_PROFILE_URL,
    "enrol/business-type/companies-house/user-account/",
)
URLs = {
    "enter your business email address and set a password": URL,
    "enter your business email address and set a password (ltd, plc or royal charter)": URL,
    "enter your business email address and set a password (sole trader or other type of business)": urljoin(
        DIRECTORY_UI_PROFILE_URL,
        "enrol/business-type/sole-trader/user-account/",
    ),
}
PAGE_TITLE = ""

SELECTORS = {
    "breadcrumbs": {
        "itself": Selector(By.CSS_SELECTOR, "nav.breadcrumbs"),
    },
    "enrolment progress bar": {"itself": Selector(By.ID, "progress-column")},
    "registration form": {
        "itself": Selector(By.CSS_SELECTOR, "section form"),
        "email": Selector(
            By.ID,
            "id_user-account-email",
            type=ElementType.INPUT,
            is_visible=False,
        ),
        "password": Selector(
            By.ID,
            "id_user-account-password",
            type=ElementType.INPUT,
            is_visible=False,
        ),
        "confirm password": Selector(
            By.ID,
            "id_user-account-password_confirmed",
            type=ElementType.INPUT,
            is_visible=False,
        ),
        "t & c": Selector(
            By.ID,
            "id_user-account-terms_agreed",
            type=ElementType.CHECKBOX,
            is_visible=False,
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
        "email": actor.email,
        "password": actor.password,
        "confirm password": actor.password,
        "t & c": True,
    }
    logging.debug(f"Generated form details: {result}")
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["registration form"]
    fill_out_input_fields(driver, form_selectors, details)
    tick_checkboxes(driver, form_selectors, details)
    tick_captcha_checkbox(driver)
    take_screenshot(driver, "After filling out the form")


def submit(driver: WebDriver) -> ModuleType:
    take_screenshot(driver, "Before submitting the form")
    find_and_click_on_page_element(
        driver, SELECTORS, "submit", wait_for_it=False
    )
    take_screenshot(driver, "After submitting the form")
    return enrol_enter_your_confirmation_code
