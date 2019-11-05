# -*- coding: utf-8 -*-
"""ERP - Summary"""
from types import ModuleType
from typing import List, Union

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
    find_and_click_on_page_element,
    submit_form,
    take_screenshot,
    tick_captcha_checkbox,
    tick_checkboxes,
)
from pages.erp import consumer_finished

NAME = "Summary"
SERVICE = Service.ERP
TYPE = PageType.FORM
URL = None
PAGE_TITLE = ""
SubURLs = {
    f"{NAME} (Developing country)": URLs.ERP_DEVELOPING_COUNTRY_SUMMARY.absolute,
    f"{NAME} (UK business)": URLs.ERP_BUSINESS_SUMMARY.absolute,
    f"{NAME} (UK importer)": URLs.ERP_IMPORTER_SUMMARY.absolute,
}
NAMES = list(SubURLs.keys())

SELECTORS = {
    "answers": {},
    "form": {
        "selection form": Selector(By.CSS_SELECTOR, "#content form[method='post']"),
        "heading": Selector(By.CSS_SELECTOR, "form[method=post] h1"),
        "t&c": Selector(
            By.ID,
            "id_summary-terms_agreed",
            type=ElementType.CHECKBOX,
            is_visible=False,
            alternative_visibility_check=True,
        ),
        "submit": Selector(
            By.CSS_SELECTOR,
            "#content > form button.govuk-button",
            type=ElementType.SUBMIT,
            next_page=consumer_finished,
        ),
    },
}
SELECTORS.update(common_selectors.ERP_HEADER)
SELECTORS.update(common_selectors.ERP_BETA)
SELECTORS.update(common_selectors.ERP_BACK)
SELECTORS.update(common_selectors.ERP_SAVE_FOR_LATER)
SELECTORS.update(common_selectors.ERP_FOOTER)


def should_be_here(driver: WebDriver, *, page_name: str = None):
    take_screenshot(driver, page_name or NAME)
    url = SubURLs[page_name]
    check_url(driver, url, exact_match=False)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)


def generate_form_details(actor: Actor, *, custom_details: dict = None) -> dict:
    result = {"t&c": True}
    if custom_details:
        result.update(custom_details)
    return result


def fill_out(driver: WebDriver, details: dict):
    tick_checkboxes(driver, SELECTORS["form"], details)
    tick_captcha_checkbox(driver)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
