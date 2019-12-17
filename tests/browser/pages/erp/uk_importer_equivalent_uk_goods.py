# -*- coding: utf-8 -*-
"""ERP - Are there equivalent goods made in the UK (UK importer)"""
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
    fill_out_textarea_fields,
    pick_one_option_and_submit,
    pick_option,
    submit_form,
)
from pages.erp import sales_volumes

NAME = "Are there equivalent goods made in the UK (UK importer)"
SERVICE = Service.ERP
TYPE = PageType.FORM
URL = URLs.ERP_IMPORTER_EQUIVALENT_UK_GOODS.absolute
PAGE_TITLE = ""

SELECTORS = {
    "form": {
        "form itself": Selector(By.CSS_SELECTOR, "#content form[method='post']"),
        "yes": Selector(
            By.CSS_SELECTOR,
            "input[value='True']",
            type=ElementType.RADIO,
            is_visible=False,
        ),
        "no": Selector(
            By.CSS_SELECTOR,
            "input[value='False']",
            type=ElementType.RADIO,
            is_visible=False,
        ),
        "tell us more": Selector(
            By.ID,
            "id_equivalent-uk-goods-equivalent_uk_goods_details",
            type=ElementType.TEXTAREA,
            is_visible=False,
        ),
        "continue": Selector(
            By.CSS_SELECTOR,
            "#content > form button.govuk-button",
            type=ElementType.SUBMIT,
            next_page=sales_volumes,
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
    equivalent_goods = choice([True, False])
    result = {"yes": equivalent_goods, "no": not equivalent_goods}

    if equivalent_goods:
        result.update({"tell us more": "filled out by AUTOMATED TESTS"})

    if custom_details:
        result.update(custom_details)
    return result


def fill_out(driver: WebDriver, details: dict):
    check_radio(driver, SELECTORS["form"], details)
    if details["yes"]:
        pick_option(driver, SELECTORS["form"], details)
        fill_out_input_fields(driver, SELECTORS["form"], details)
        fill_out_textarea_fields(driver, SELECTORS["form"], details)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
