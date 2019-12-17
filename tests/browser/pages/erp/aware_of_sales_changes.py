# -*- coding: utf-8 -*-
"""ERP - Are you aware of sales changes"""
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

NAME = "Are you aware of sales changes"
SERVICE = Service.ERP
TYPE = PageType.FORM
URL = None
PAGE_TITLE = ""
SubURLs = {
    f"{NAME} (Developing country)": URLs.ERP_DEVELOPING_COUNTRY_SALES_AFTER_BREXIT.absolute,
    f"{NAME} (UK business)": URLs.ERP_BUSINESS_SALES_AFTER_BREXIT.absolute,
    f"{NAME} (UK importer)": URLs.ERP_IMPORTER_SALES_AFTER_BREXIT.absolute,
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
        "aware of volume changes": Selector(
            By.ID,
            "id_sales-after-brexit-has_volume_changed_0",
            type=ElementType.RADIO,
            is_visible=False,
            alternative_visibility_check=True,
        ),
        "not aware of volume changes": Selector(
            By.ID,
            "id_sales-after-brexit-has_volume_changed_1",
            type=ElementType.RADIO,
            is_visible=False,
            alternative_visibility_check=True,
        ),
        "actual change in volume": Selector(
            By.ID,
            "id_sales-after-brexit-volume_changed_type_0",
            type=ElementType.CHECKBOX,
            is_visible=False,
        ),
        "expected change in volume": Selector(
            By.ID,
            "id_sales-after-brexit-volume_changed_type_1",
            type=ElementType.CHECKBOX,
            is_visible=False,
        ),
        "tell us more about volume changes": Selector(
            By.ID,
            "id_sales-after-brexit-volumes_change_comment",
            type=ElementType.TEXTAREA,
            is_visible=False,
        ),
        "aware of price changes": Selector(
            By.ID,
            "id_sales-after-brexit-has_price_changed_0",
            type=ElementType.RADIO,
            is_visible=False,
            alternative_visibility_check=True,
        ),
        "not aware of price changes": Selector(
            By.ID,
            "id_sales-after-brexit-has_price_changed_1",
            type=ElementType.RADIO,
            is_visible=False,
            alternative_visibility_check=True,
        ),
        "actual change in price": Selector(
            By.ID,
            "id_sales-after-brexit-price_changed_type_0",
            type=ElementType.CHECKBOX,
            is_visible=False,
        ),
        "expected change in price": Selector(
            By.ID,
            "id_sales-after-brexit-price_changed_type_1",
            type=ElementType.CHECKBOX,
            is_visible=False,
        ),
        "tell us more about price changes": Selector(
            By.ID,
            "id_sales-after-brexit-price_change_comment",
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


def should_be_here(driver: WebDriver, *, page_name: str = None):
    url = SubURLs[page_name]
    check_url(driver, url, exact_match=False)


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
    aware_of_volume_changes = choice([True, False])
    not_aware_of_volume_changes = not aware_of_volume_changes

    result = {
        "aware of volume changes": aware_of_volume_changes,
        "not aware of volume changes": not_aware_of_volume_changes,
        "aware of price changes": aware_of_price_changes,
        "not aware of price changes": not_aware_of_price_changes,
    }

    if aware_of_volume_changes:
        actual = choice([True, False])
        expected = choice([True, False]) if actual else True
        result.update(
            {
                "actual change in volume": actual,
                "expected change in volume": expected,
                "tell us more about volume changes": "Automated Test",
            }
        )
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
