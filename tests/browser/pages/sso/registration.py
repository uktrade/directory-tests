# -*- coding: utf-8 -*-
"""SSO Registration Page Object."""
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType, Services, common_selectors
from pages.common_actions import (
    Actor,
    Selector,
    check_for_sections,
    check_url,
    fill_out_input_fields,
    find_and_click_on_page_element,
    find_element,
    go_to_url,
    take_screenshot,
    tick_checkboxes,
    try_js_click_on_element_click_intercepted_exception,
    wait_for_page_load_after_action,
)
from settings import DIRECTORY_UI_SSO_URL

NAME = "Registration"
SERVICE = Services.SSO
TYPE = "registration"
URL = urljoin(DIRECTORY_UI_SSO_URL, "accounts/signup/")
PAGE_TITLE = "Register - great.gov.uk"

SEND_BUTTON = Selector(
    By.CSS_SELECTOR, "#signup_form > button", type=ElementType.BUTTON
)
SELECTORS = {
    "form": {
        "title": Selector(By.CSS_SELECTOR, "#profile-register-intro > h1"),
        "email": Selector(By.ID, "id_email", type=ElementType.INPUT),
        "confirm email": Selector(By.ID, "id_email2", type=ElementType.INPUT),
        "password": Selector(By.ID, "id_password1", type=ElementType.INPUT),
        "confirm password": Selector(By.ID, "id_password2", type=ElementType.INPUT),
        "t&c": Selector(
            By.ID, "id_terms_agreed", is_visible=False, type=ElementType.CHECKBOX
        ),
        "sign up button": SEND_BUTTON,
    }
}
SELECTORS.update(common_selectors.HEADER)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.SSO_LOGGED_OUT)
SELECTORS.update(common_selectors.FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)


def generate_form_details(actor: Actor, *, custom_details: dict = None) -> dict:
    result = {
        "email": actor.email,
        "confirm email": actor.email,
        "password": actor.password,
        "confirm password": actor.password,
        "t&c": True,
    }
    if custom_details:
        result.update(custom_details)
    return result


def fill_out(driver: WebDriver, contact_us_details: dict):
    form_selectors = SELECTORS["form"]
    fill_out_input_fields(driver, form_selectors, contact_us_details)
    tick_checkboxes(driver, form_selectors, contact_us_details)
    take_screenshot(driver, NAME + "after filling out the form")


def submit(driver: WebDriver):
    take_screenshot(driver, "Before submitting the contact supplier form")
    sign_up_button = find_element(
        driver, SEND_BUTTON, element_name="Send button", wait_for_it=False
    )
    with try_js_click_on_element_click_intercepted_exception(driver, sign_up_button):
        sign_up_button.click()


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)
