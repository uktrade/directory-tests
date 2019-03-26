# -*- coding: utf-8 -*-
"""Export Readiness - First page of Long SOO Contact us form"""
from types import ModuleType
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Actor,
    Selector,
    check_random_radio,
    check_url,
    fill_out_input_fields,
    fill_out_textarea_fields,
    find_element,
    go_to_url,
    take_screenshot,
)
from pages.exred import contact_us_soo_long_contact_details
from settings import EXRED_UI_URL

NAME = "Long Domestic (Your experience)"
SERVICE = "Export Readiness"
TYPE = "Contact us"
URL = urljoin(EXRED_UI_URL, "contact/selling-online-overseas/your-experience/")
PAGE_TITLE = "Welcome to great.gov.uk"

SUBMIT_BUTTON = Selector(
    By.CSS_SELECTOR, "form button[type=submit]", type=ElementType.BUTTON
)
SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#content form"),
        "not yet": Selector(
            By.ID, "id_your-experience-experience_0", type=ElementType.RADIO
        ),
        "yes, sometimes": Selector(
            By.ID, "id_your-experience-experience_1", type=ElementType.RADIO
        ),
        "yes, regularly": Selector(
            By.ID, "id_your-experience-experience_2", type=ElementType.RADIO
        ),
        "description": Selector(
            By.ID, "id_your-experience-description", type=ElementType.TEXTAREA
        ),
    }
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL)


def generate_form_details(actor: Actor) -> dict:
    return {"description": "automated tests"}


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    check_random_radio(driver, form_selectors)
    fill_out_input_fields(driver, form_selectors, details)
    fill_out_textarea_fields(driver, form_selectors, details)
    take_screenshot(driver, "After filling out the form")


def submit(driver: WebDriver) -> ModuleType:
    take_screenshot(driver, "Before submitting the form")
    button = find_element(
        driver, SUBMIT_BUTTON, element_name="Submit button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, "After submitting the form")
    return contact_us_soo_long_contact_details
