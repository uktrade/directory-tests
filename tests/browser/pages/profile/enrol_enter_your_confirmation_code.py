# -*- coding: utf-8 -*-
"""Profile - Enrol - Enter your confirmation code"""
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Selector,
    check_url,
    go_to_url,
    take_screenshot,
    find_and_click_on_page_element,
    check_for_sections,
    Actor,
    fill_out_input_fields
)
from settings import DIRECTORY_UI_PROFILE_URL

NAME = "Enter your confirmation code"
SERVICE = "Profile"
TYPE = "Enrol"
URL = urljoin(DIRECTORY_UI_PROFILE_URL, "enrol/business-type/companies-house/verification/")
PAGE_TITLE = ""

SELECTORS = {
    "enrolment progress bar": {
        "itself": Selector(By.ID, "progress-column"),
    },
    "confirmation code message": {
        "message": Selector(
            By.CSS_SELECTOR, "#user-account-verification-header-container p"
        ),
    },
    "an option to resend the code": {
        "resend my code": Selector(By.CSS_SELECTOR, "section form a"),
    },
    "confirmation code form": {
        "itself": Selector(By.CSS_SELECTOR, "section form"),
        "code": Selector(
            By.ID, "id_verification-code", type=ElementType.INPUT
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
    check_url(driver, URL)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)


def generate_form_details(actor: Actor) -> dict:
    return {"code": actor.email_confirmation_code}


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["confirmation code form"]
    fill_out_input_fields(driver, form_selectors, details)
    take_screenshot(driver, "After filling out the form")


def submit(driver: WebDriver):
    take_screenshot(driver, "Before submitting the form")
    find_and_click_on_page_element(driver, SELECTORS, "submit", wait_for_it=False)
    take_screenshot(driver, "After submitting the form")
