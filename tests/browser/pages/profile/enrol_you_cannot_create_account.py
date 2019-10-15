# -*- coding: utf-8 -*-
"""Profile - Enrol - You cannot create an account page"""
import logging
from types import ModuleType
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import Service
from pages import common_selectors
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

NAME = "You cannot create an account"
SERVICE = Service.PROFILE
TYPE = "Enrol"
URL = URLs.PROFILE_ENROL_OVERSEAS_BUSINESS.absolute
PAGE_TITLE = ""

SELECTORS = {
    "explanation": {
        "heading": Selector(By.CSS_SELECTOR, "#content div > h1"),
        "back": Selector(By.PARTIAL_LINK_TEXT, "Back"),
        "visit our site for international businesses": Selector(
            By.PARTIAL_LINK_TEXT, "visit our site for international businesses."
        ),
    }
}
SELECTORS.update(common_selectors.HEADER)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL)
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


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)
