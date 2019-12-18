# -*- coding: utf-8 -*-
"""ERP - Market size"""
from random import choice, randrange
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
    pick_one_option_and_submit,
    pick_option,
    submit_form,
)

NAME = "Market size"
SERVICE = Service.ERP
TYPE = PageType.FORM
URL = None
PAGE_TITLE = ""
SubURLs = {
    f"{NAME} (UK business)": URLs.ERP_BUSINESS_MARKET_SIZE.absolute,
    f"{NAME} (UK importer)": URLs.ERP_IMPORTER_MARKET_SIZE.absolute,
}
SubURLs = {key.lower(): val for key, val in SubURLs.items()}
NAMES = list(SubURLs.keys())

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
        "financial year": Selector(
            By.ID,
            "id_market-size-market_size_year",
            type=ElementType.SELECT,
            is_visible=False,
        ),
        "market value": Selector(
            By.ID,
            "id_market-size-market_size",
            type=ElementType.INPUT,
            is_visible=False,
        ),
        "continue": Selector(
            By.CSS_SELECTOR,
            "#content > form button.govuk-button",
            type=ElementType.SUBMIT,
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
    know_market_value = choice([True, False])
    result = {"yes": know_market_value, "no": not know_market_value}

    if know_market_value:
        result.update({"financial year": None, "market value": randrange(0, 99999)})

    if custom_details:
        result.update(custom_details)
    return result


def fill_out(driver: WebDriver, details: dict):
    check_radio(driver, SELECTORS["form"], details)
    if details["yes"]:
        pick_option(driver, SELECTORS["form"], details)
        fill_out_input_fields(driver, SELECTORS["form"], details)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
