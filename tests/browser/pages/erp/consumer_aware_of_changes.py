# -*- coding: utf-8 -*-
"""ERP - Are you aware of changes (UK consumer)"""
import logging
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
    pick_one_option_and_submit,
    submit_form,
    tick_checkboxes,
)
from pages.erp import consumer_other_changes_after_brexit

NAME = "Are you aware of changes (UK consumer)"
SERVICE = Service.ERP
TYPE = PageType.FORM
URL = URLs.ERP_CONSUMER_CHANGE.absolute
PAGE_TITLE = ""

SELECTORS = {
    "form": {
        "selection form": Selector(By.CSS_SELECTOR, "#content form[method='post']"),
        "step counter": Selector(
            By.CSS_SELECTOR, "form[method=post] span.govuk-caption-l"
        ),
        "heading": Selector(By.CSS_SELECTOR, "form[method=post] h1"),
        "aware of price changes": Selector(
            By.ID,
            "id_consumer-change-has_consumer_price_changed_0",
            type=ElementType.RADIO,
            is_visible=False,
        ),
        "not aware of price changes": Selector(
            By.ID,
            "id_consumer-change-has_consumer_price_changed_1",
            type=ElementType.RADIO,
            is_visible=False,
        ),
        "actual change in price": Selector(
            By.ID,
            "id_consumer-change-price_changed_type_0",
            type=ElementType.CHECKBOX,
            is_visible=False,
        ),
        "expected change in price": Selector(
            By.ID,
            "id_consumer-change-price_changed_type_1",
            type=ElementType.CHECKBOX,
            is_visible=False,
        ),
        "tell us more about price changes": Selector(
            By.ID,
            "id_consumer-change-price_change_comment",
            type=ElementType.TEXTAREA,
            is_visible=False,
        ),
        "aware of choice changes": Selector(
            By.ID,
            "id_consumer-change-has_consumer_choice_changed_0",
            type=ElementType.RADIO,
            is_visible=False,
        ),
        "not aware of choice changes": Selector(
            By.ID,
            "id_consumer-change-has_consumer_choice_changed_1",
            type=ElementType.RADIO,
            is_visible=False,
        ),
        "actual change in choice": Selector(
            By.ID,
            "id_consumer-change-choice_change_type_0",
            type=ElementType.CHECKBOX,
            is_visible=False,
        ),
        "expected change in choice": Selector(
            By.ID,
            "id_consumer-change-choice_change_type_1",
            type=ElementType.CHECKBOX,
            is_visible=False,
        ),
        "tell us more about choice changes": Selector(
            By.ID,
            "id_consumer-change-choice_change_comment",
            type=ElementType.TEXTAREA,
            is_visible=False,
        ),
        "continue": Selector(
            By.CSS_SELECTOR,
            "#content > form button.govuk-button",
            type=ElementType.SUBMIT,
            next_page=consumer_other_changes_after_brexit,
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


def pick_radio_option_and_submit(driver: WebDriver, name: str) -> ModuleType:
    return pick_one_option_and_submit(
        driver, SELECTORS["form"], name, submit_button_name="continue"
    )


def generate_form_details(actor: Actor, *, custom_details: dict = None) -> dict:
    aware_of_price_changes = choice([True, False])
    not_aware_of_price_changes = not aware_of_price_changes
    aware_of_choice_changes = choice([True, False])
    not_aware_of_choice_changes = not aware_of_choice_changes

    result = {
        "aware of price changes": aware_of_price_changes,
        "not aware of price changes": not_aware_of_price_changes,
        "aware of choice changes": aware_of_choice_changes,
        "not aware of choice changes": not_aware_of_choice_changes,
    }

    if aware_of_price_changes:
        actual = choice([True, False])
        expected = choice([True, False]) if actual else True
        result.update(
            {
                "actual change in price": actual,
                "expected change in price": expected,
                "tell us more about price changes": "Automated Test",
            }
        )
    if aware_of_choice_changes:
        actual = choice([True, False])
        expected = choice([True, False]) if actual else True
        result.update(
            {
                "actual change in choice": actual,
                "expected change in choice": expected,
                "tell us more about choice changes": "Automated Test",
            }
        )

    if custom_details:
        result.update(custom_details)

    logging.debug(f"Generated form details: {result}")
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    check_radio(driver, form_selectors, details)
    tick_checkboxes(driver, form_selectors, details)
    fill_out_textarea_fields(driver, form_selectors, details)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
