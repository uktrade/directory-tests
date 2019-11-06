# -*- coding: utf-8 -*-
"""Profile - Enrol - Enter your confirmation code (UK taxpayer)"""
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
    go_to_url,
    submit_form,
    take_screenshot,
)

NAME = "Enter your confirmation code (UK taxpayer)"
SERVICE = Service.PROFILE
TYPE = PageType.FORM
URL = URLs.PROFILE_ENROL_INDIVIDUAL_EMAIL_VERIFICATION.absolute
PAGE_TITLE = ""

SELECTORS = {
    "enrolment progress bar": {"itself": Selector(By.ID, "progress-column")},
    "confirmation code message": {
        "message": Selector(
            By.CSS_SELECTOR, "#user-account-verification-header-container p"
        )
    },
    "an option to resend the code": {
        "resend my code": Selector(By.CSS_SELECTOR, "section form a")
    },
    "confirmation code form": {
        "itself": Selector(By.CSS_SELECTOR, "section form"),
        "code": Selector(By.ID, "id_verification-code", type=ElementType.INPUT),
        "submit": Selector(
            By.CSS_SELECTOR, "form button.button", type=ElementType.SUBMIT
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


def generate_form_details(actor: Actor) -> dict:
    return {"code": actor.email_confirmation_code}


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["confirmation code form"]
    fill_out_input_fields(driver, form_selectors, details)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["confirmation code form"])
