# -*- coding: utf-8 -*-
"""ERP - Are you aware of other changes"""
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
    fill_out_textarea_fields,
    submit_form,
    tick_checkboxes,
)
from pages.erp import consumer_type

NAME = "Are you aware of other changes"
SERVICE = Service.ERP
TYPE = PageType.FORM
URL = URLs.ERP_CONSUMER_OTHER_CHANGES_AFTER_BREXIT.absolute
PAGE_TITLE = ""
SubURLs = {
    f"{NAME} (Developing country)": URLs.ERP_DEVELOPING_COUNTRY_OTHER_CHANGES_AFTER_BREXIT.absolute,
    f"{NAME} (UK business)": URLs.ERP_BUSINESS_OTHER_CHANGES_AFTER_BREXIT.absolute,
    f"{NAME} (UK importer)": URLs.ERP_IMPORTER_OTHER_CHANGES_AFTER_BREXIT.absolute,
}
SubURLs = {key.lower(): val for key, val in SubURLs.items()}
NAMES = list(SubURLs.keys())

SELECTORS = {
    "form": {
        "selection form": Selector(By.CSS_SELECTOR, "#content form[method='post']"),
        "step counter": Selector(
            By.CSS_SELECTOR, "form[method=post] span.govuk-caption-l"
        ),
        "heading": Selector(By.CSS_SELECTOR, "form[method=post] h1"),
        "aware of other changes": Selector(
            By.ID,
            "id_other-changes-after-brexit-has_other_changes_0",
            type=ElementType.RADIO,
            is_visible=False,
            alternative_visibility_check=True,
        ),
        "not aware of other changes": Selector(
            By.ID,
            "id_other-changes-after-brexit-has_other_changes_1",
            type=ElementType.RADIO,
            is_visible=False,
            alternative_visibility_check=True,
        ),
        "actual change": Selector(
            By.ID,
            "id_other-changes-after-brexit-has_other_changes_type_0",
            type=ElementType.CHECKBOX,
            is_visible=False,
        ),
        "expected change": Selector(
            By.ID,
            "id_other-changes-after-brexit-has_other_changes_type_1",
            type=ElementType.CHECKBOX,
            is_visible=False,
        ),
        "tell us more about changes": Selector(
            By.ID,
            "id_other-changes-after-brexit-other_changes_comment",
            type=ElementType.TEXTAREA,
            is_visible=False,
        ),
        "comment": Selector(
            By.ID,
            "id_other-changes-after-brexit-other_information",
            type=ElementType.TEXTAREA,
        ),
        "continue": Selector(
            By.CSS_SELECTOR,
            "#content > form button.govuk-button",
            type=ElementType.SUBMIT,
            next_page=consumer_type,
        ),
    }
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


def should_see_form_choices(driver: WebDriver, names: List[str]):
    check_form_choices(driver, SELECTORS["form"], names)


def generate_form_details(actor: Actor, *, custom_details: dict = None) -> dict:
    aware_or_not = choice([True, False])
    result = {
        "comment": "Filled out and submitted by AUTOMATED TESTS",
        "aware of other changes": aware_or_not,
        "not aware of other changes": not aware_or_not,
    }

    if aware_or_not:
        actual = choice([True, False])
        expected = choice([True, False]) if actual else True
        result.update(
            {
                "actual change": actual,
                "expected change": expected,
                "tell us more about changes": "Automated Test",
            }
        )
    if custom_details:
        result.update(custom_details)
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    check_radio(driver, form_selectors, details)
    tick_checkboxes(driver, form_selectors, details)
    fill_out_textarea_fields(driver, form_selectors, details)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
