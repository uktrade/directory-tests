# -*- coding: utf-8 -*-
"""ERP - Business details"""
from random import choice
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
    check_form_choices,
    check_radio,
    check_url,
    fill_out_input_fields,
    pick_option,
    submit_form,
)
from pages.erp import summary

NAME = "Business details (Developing country)"
SERVICE = Service.ERP
TYPE = PageType.FORM
URL = URLs.ERP_DEVELOPING_COUNTRY_BUSINESS_DETAILS.absolute
PAGE_TITLE = ""


SELECTORS = {
    "form": {
        "selection form": Selector(By.CSS_SELECTOR, "#content form[method='post']"),
        "step counter": Selector(
            By.CSS_SELECTOR, "form[method=post] span.govuk-caption-l"
        ),
        "heading": Selector(By.CSS_SELECTOR, "form[method=post] h1"),
        "company name": Selector(
            By.ID, "id_business-company_name", type=ElementType.INPUT
        ),
        "industry": Selector(By.ID, "id_business-sector", type=ElementType.SELECT),
        "company size": Selector(
            By.ID, "id_business-employees", type=ElementType.SELECT
        ),
        "annual turnover": Selector(
            By.ID, "id_business-turnover", type=ElementType.SELECT
        ),
        "continue": Selector(
            By.CSS_SELECTOR,
            "#content > form button.govuk-button",
            type=ElementType.SUBMIT,
            next_page=summary,
        ),
    }
}
SELECTORS.update(common_selectors.ERP_HEADER)
SELECTORS.update(common_selectors.ERP_BETA)
SELECTORS.update(common_selectors.ERP_BACK)
SELECTORS.update(common_selectors.ERP_SAVE_FOR_LATER)
SELECTORS.update(common_selectors.ERP_FOOTER)


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=False)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def should_see_form_choices(driver: WebDriver, names: List[str]):
    check_form_choices(driver, SELECTORS["form"], names)


def generate_form_details(actor: Actor, *, custom_details: dict = None) -> dict:
    private_or_other = choice([True, False])
    result = {
        "uk private or public limited company": private_or_other,
        "other type of uk organisation": not private_or_other,
        "company name": "AUTOMATED TESTS",
        "industry": None,
        "company size": None,
        "annual turnover": None,
        "regions": True,
    }
    if custom_details:
        result.update(custom_details)
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    check_radio(driver, form_selectors, details)
    pick_option(driver, form_selectors, details)
    fill_out_input_fields(driver, form_selectors, details)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
