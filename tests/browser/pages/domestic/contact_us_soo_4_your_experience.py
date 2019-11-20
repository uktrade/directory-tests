# -*- coding: utf-8 -*-
"""Domestic - 4/4 page of Long SOO Contact us form"""
from types import ModuleType
from typing import Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType, common_selectors
from pages.common_actions import (
    Actor,
    Selector,
    check_random_radio,
    check_url,
    fill_out_textarea_fields,
    go_to_url,
    submit_form,
    take_screenshot,
)
from pages.domestic import contact_us_soo_5_thank_you

NAME = "Your experience (SOO)"
SERVICE = Service.DOMESTIC
TYPE = PageType.CONTACT_US
URL = URLs.CONTACT_US_SOO_ORGANISATION_YOUR_EXPERIENCE.absolute
PAGE_TITLE = "Welcome to great.gov.uk"

SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#content form"),
        "not yet": Selector(
            By.ID, "id_your-experience-experience_0", type=ElementType.RADIO, group_id=1
        ),
        "yes, sometimes": Selector(
            By.ID, "id_your-experience-experience_1", type=ElementType.RADIO, group_id=1
        ),
        "yes, regularly": Selector(
            By.ID, "id_your-experience-experience_2", type=ElementType.RADIO, group_id=1
        ),
        "description": Selector(
            By.ID, "id_your-experience-description", type=ElementType.TEXTAREA
        ),
        "submit": Selector(
            By.CSS_SELECTOR,
            "form button.button[type=submit]",
            type=ElementType.SUBMIT,
            next_page=contact_us_soo_5_thank_you,
        ),
    }
}
SELECTORS.update(common_selectors.DOMESTIC_HEADER)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.DOMESTIC_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL)


def generate_form_details(actor: Actor) -> dict:
    return {"description": "this SOO form was submitted by automated tests"}


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    check_random_radio(driver, form_selectors)
    fill_out_textarea_fields(driver, form_selectors, details)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
