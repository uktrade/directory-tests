# -*- coding: utf-8 -*-
"""ERP - Summary - UK consumer"""
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
)
from pages.erp import consumer_finished

NAME = "Summary (UK consumer)"
SERVICE = Service.ERP
TYPE = PageType.FORM
URL = URLs.ERP_CONSUMER_SUMMARY.absolute
PAGE_TITLE = ""

SELECTORS = {
    "form": {
        "selection form": Selector(By.CSS_SELECTOR, "#content form[method='post']"),
        "step counter": Selector(
            By.CSS_SELECTOR, "form[method=post] span.govuk-caption-l"
        ),
        "heading": Selector(By.CSS_SELECTOR, "form[method=post] h1"),
        "submit": Selector(
            By.CSS_SELECTOR,
            "#content > form button.govuk-button",
            type=ElementType.SUBMIT,
            next_page=consumer_finished,
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


def generate_form_details(actor: Actor, *, custom_details: dict = None) -> dict:
    return {}


def fill_out(driver: WebDriver, details: dict):
    tick_captcha_checkbox(driver)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
