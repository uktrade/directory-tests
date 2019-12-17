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
    pick_option,
    submit_form,
)
from pages.erp import summary

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


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
