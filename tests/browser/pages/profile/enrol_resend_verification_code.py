# -*- coding: utf-8 -*-
"""Profile - Enrol - Resend your verification code"""
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType, Services
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
from settings import DIRECTORY_UI_PROFILE_URL

NAME = "Resend your verification code"
SERVICE = Services.PROFILE
TYPE = "Enrol"
URL = urljoin(
    DIRECTORY_UI_PROFILE_URL, "enrol/resend-verification/resend/"
)
PAGE_TITLE = ""

SELECTORS = {
    "form": {
        "form": Selector(By.CSS_SELECTOR, "form[method=POST]"),
        "email": Selector(By.ID, "id_resend-email", type=ElementType.INPUT),
        "if the resent code doesn't work": Selector(By.CSS_SELECTOR, "form > div > p > a.link"),
        "submit": Selector(By.CSS_SELECTOR, "form button.button", type=ElementType.BUTTON),
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
    return {"email": actor.email}


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    fill_out_input_fields(driver, form_selectors, details)
    take_screenshot(driver, "After filling out the form")


def submit(driver: WebDriver):
    take_screenshot(driver, "Before submitting the form")
    find_and_click_on_page_element(driver, SELECTORS, "submit", wait_for_it=False)
    take_screenshot(driver, "After submitting the form")
