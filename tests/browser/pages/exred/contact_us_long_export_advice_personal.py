# -*- coding: utf-8 -*-
"""Export Readiness - First page of Long Contact us form"""
from types import ModuleType
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Actor,
    Selector,
    check_url,
    fill_out_input_fields,
    find_element,
    go_to_url,
    take_screenshot,
)
from pages.exred import contact_us_long_export_advice_business
from settings import EXRED_UI_URL

NAME = "Long (Personal details)"
SERVICE = "Export Readiness"
TYPE = "Contact us"
URL = urljoin(EXRED_UI_URL, "contact/export-advice/personal/")
PAGE_TITLE = "Welcome to great.gov.uk"

SUBMIT_BUTTON = Selector(
    By.CSS_SELECTOR, "div.exred-triage-form button", type=ElementType.BUTTON
)
SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#lede form"),
        "first name": Selector(By.ID, "id_personal-first_name", type=ElementType.INPUT),
        "last name": Selector(By.ID, "id_personal-last_name", type=ElementType.INPUT),
        "position": Selector(By.ID, "id_personal-position", type=ElementType.INPUT),
        "email": Selector(By.ID, "id_personal-email", type=ElementType.INPUT),
        "phone": Selector(By.ID, "id_personal-phone", type=ElementType.INPUT),
        "submit": SUBMIT_BUTTON,
    }
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL)


def generate_form_details(actor: Actor) -> dict:
    result = {
        "first name": f"send by {actor.alias} - automated tests",
        "last name": actor.alias,
        "position": "automated tests",
        "email": actor.email,
        "phone": "automated tests",
    }
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    fill_out_input_fields(driver, form_selectors, details)
    take_screenshot(driver, "After filling out the form")


def submit(driver: WebDriver) -> ModuleType:
    take_screenshot(driver, "Before submitting the form")
    button = find_element(
        driver, SUBMIT_BUTTON, element_name="Submit button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, "After submitting the form")
    return contact_us_long_export_advice_business
