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
    submit_form,
    tick_captcha_checkbox,
)
from pages.erp import finished

NAME = "Summary"
SERVICE = Service.ERP
TYPE = PageType.FORM
URL = None
PAGE_TITLE = ""
SubURLs = {
    f"{NAME} (Developing country)": URLs.ERP_DEVELOPING_COUNTRY_SUMMARY.absolute,
    f"{NAME} (UK business)": URLs.ERP_BUSINESS_SUMMARY.absolute,
    f"{NAME} (UK importer)": URLs.ERP_IMPORTER_SUMMARY.absolute,
    f"{NAME} (UK consumer)": URLs.ERP_CONSUMER_SUMMARY.absolute,
}
SubURLs = {key.lower(): val for key, val in SubURLs.items()}
NAMES = list(SubURLs.keys())

SELECTORS = {
    "answers": {},
    "form": {
        "selection form": Selector(By.CSS_SELECTOR, "#content form[method='post']"),
        "heading": Selector(By.CSS_SELECTOR, "form[method=post] h1"),
        "submit": Selector(
            By.CSS_SELECTOR,
            "#content > form button.govuk-button",
            type=ElementType.SUBMIT,
            next_page=finished,
        ),
    },
}
SELECTORS.update(common_selectors.ERP_HEADER)
SELECTORS.update(common_selectors.ERP_BETA)
SELECTORS.update(common_selectors.ERP_BACK)
SELECTORS.update(common_selectors.ERP_SAVE_FOR_LATER)
SELECTORS.update(common_selectors.ERP_FOOTER)


def should_be_here(driver: WebDriver, *, page_name: str = None):
    url = SubURLs[page_name]
    check_url(driver, url, exact_match=False)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def generate_form_details(actor: Actor, *, custom_details: dict = None) -> dict:
    return {}


def fill_out(driver: WebDriver, details: dict):
    tick_captcha_checkbox(driver)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])


def should_see_correct_data_on_summary_page(driver: WebDriver, forms_data: dict):
    pass
