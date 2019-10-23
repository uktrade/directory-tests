# -*- coding: utf-8 -*-
"""ERP - Personal details - UK consumer"""
from types import ModuleType
from typing import List, Union
from uuid import uuid4

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType, common_selectors
from pages.common_actions import (
    Actor,
    Selector,
    check_for_sections,
    check_url,
    fill_out_input_fields,
    find_and_click_on_page_element,
    pick_option,
    submit_form,
    take_screenshot,
)
from pages.erp import consumer_summary

NAME = "Personal details (UK consumer)"
SERVICE = Service.ERP
TYPE = PageType.FORM
URL = URLs.ERP_CONSUMER_PERSONAL.absolute
PAGE_TITLE = ""

SELECTORS = {
    "form": {
        "selection form": Selector(By.CSS_SELECTOR, "#content form[method='post']"),
        "step counter": Selector(
            By.CSS_SELECTOR, "form[method=post] span.govuk-caption-l"
        ),
        "heading": Selector(By.CSS_SELECTOR, "form[method=post] h1"),
        "given mane": Selector(By.ID, "id_personal-given_name", type=ElementType.INPUT),
        "family mane": Selector(
            By.ID, "id_personal-family_name", type=ElementType.INPUT
        ),
        "email": Selector(By.ID, "id_personal-email", type=ElementType.INPUT),
        "income bracket": Selector(
            By.ID, "id_personal-income_bracket", type=ElementType.SELECT
        ),
        "consumer region": Selector(
            By.ID, "id_personal-consumer_region", type=ElementType.SELECT
        ),
        "continue": Selector(
            By.CSS_SELECTOR,
            "#content > form button.govuk-button",
            type=ElementType.SUBMIT,
            next_page=consumer_summary,
        ),
    }
}
SELECTORS.update(common_selectors.ERP_HEADER)
SELECTORS.update(common_selectors.ERP_BETA)
SELECTORS.update(common_selectors.ERP_BACK)
SELECTORS.update(common_selectors.ERP_SAVE_FOR_LATER)
SELECTORS.update(common_selectors.ERP_FOOTER)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)


def generate_form_details(actor: Actor, *, custom_details: dict = None) -> dict:
    result = {
        "given mane": actor.alias,
        "family mane": str(uuid4()),
        "email": actor.email,
        "income bracket": None,
        "consumer region": None,
    }
    if custom_details:
        result.update(custom_details)
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    fill_out_input_fields(driver, form_selectors, details)
    pick_option(driver, form_selectors, details)
    take_screenshot(driver, "After filling out the form")


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
