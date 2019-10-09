# -*- coding: utf-8 -*-
"""Profile - Enrol - UK taxpayer - Enter your email address and set a password"""
import logging
from types import ModuleType
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import Service
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

NAME = "Enter your email address and set a password (UK taxpayer)"
SERVICE = Service.PROFILE
TYPE = "Enrol"
URL = URLs.PROFILE_ENROL_INDIVIDUAL_ENTER_YOUR_EMAIL_AND_PASSWORD.absolute
PAGE_TITLE = ""

SELECTORS = {
    "breadcrumbs": {"itself": Selector(By.CSS_SELECTOR, "nav.breadcrumbs")},
    "enrolment progress bar": {"itself": Selector(By.ID, "progress-column")},
    "registration form": {
        "itself": Selector(By.CSS_SELECTOR, "section form"),
        "email": Selector(
            By.ID, "id_user-account-email", type=ElementType.INPUT, is_visible=False
        ),
        "password": Selector(
            By.ID, "id_user-account-password", type=ElementType.INPUT, is_visible=False
        ),
        "confirm password": Selector(
            By.ID,
            "id_user-account-password_confirmed",
            type=ElementType.INPUT,
            is_visible=False,
        ),
        "t & c": Selector(
            By.ID,
            "id_user-account-terms_agreed-label",
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


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
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
    find_and_click_on_page_element(driver, SELECTORS, "submit", wait_for_it=False)
    take_screenshot(driver, "After submitting the form")
    return enrol_enter_your_confirmation_code
