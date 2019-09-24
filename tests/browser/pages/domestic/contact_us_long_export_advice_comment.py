# -*- coding: utf-8 -*-
"""Domestic - First page of Long Contact us form"""
from types import ModuleType
from urllib.parse import urljoin

from directory_tests_shared.enums import Service
from directory_tests_shared.settings import DOMESTIC_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Actor,
    Selector,
    check_url,
    fill_out_textarea_fields,
    find_element,
    go_to_url,
    take_screenshot,
)
from pages.domestic import contact_us_long_export_advice_personal

NAME = "Long (Export Advice Comment)"
SERVICE = Service.DOMESTIC
TYPE = "Contact us"
URL = urljoin(DOMESTIC_URL, "contact/export-advice/comment/")
PAGE_TITLE = "Welcome to great.gov.uk"

SUBMIT_BUTTON = Selector(
    By.CSS_SELECTOR, "div.exred-triage-form button", type=ElementType.BUTTON
)
SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#lede form"),
        "comment": Selector(By.ID, "id_comment-comment", type=ElementType.TEXTAREA),
        "submit": SUBMIT_BUTTON,
    }
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL)


def generate_form_details(actor: Actor) -> dict:
    result = {"comment": f"Submitted by automated tests {actor.alias}"}
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    fill_out_textarea_fields(driver, form_selectors, details)
    take_screenshot(driver, "After filling out the form")


def submit(driver: WebDriver) -> ModuleType:
    take_screenshot(driver, "Before submitting the form")
    button = find_element(
        driver, SUBMIT_BUTTON, element_name="Submit button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, "After submitting the form")
    return contact_us_long_export_advice_personal
