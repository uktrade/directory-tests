# -*- coding: utf-8 -*-
"""ERP - Country select - Developing Country """
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
    check_url,
    fill_out_input_fields,
    find_element,
    go_to_url,
    pick_one_option_and_submit,
    submit_form,
)
from pages.erp import product_search
from pages.erp.autocomplete_callbacks import autocomplete_country

NAME = "Select country (Developing country)"
SERVICE = Service.ERP
TYPE = PageType.FORM
URL = URLs.ERP_DEVELOPING_COUNTRY.absolute
PAGE_TITLE = ""

SELECTORS = {
    "form": {
        "form itself": Selector(By.CSS_SELECTOR, "#content form[method='post']"),
        "country": Selector(
            By.ID,
            "id_country-country",
            type=ElementType.INPUT,
            is_visible=False,
            autocomplete_callback=autocomplete_country,
        ),
        "continue": Selector(
            By.CSS_SELECTOR,
            "#content > form button.govuk-button",
            type=ElementType.SUBMIT,
            next_page=product_search,
        ),
    }
}
SELECTORS.update(common_selectors.ERP_HEADER)
SELECTORS.update(common_selectors.ERP_BETA)
SELECTORS.update(common_selectors.ERP_BACK)
SELECTORS.update(common_selectors.ERP_BREADCRUMBS)
SELECTORS.update(common_selectors.ERP_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def should_see_form_choices(driver: WebDriver, names: List[str]):
    check_form_choices(driver, SELECTORS["form"], names)


def pick_radio_option_and_submit(driver: WebDriver, name: str) -> ModuleType:
    return pick_one_option_and_submit(
        driver, SELECTORS["form"], name, submit_button_name="continue"
    )


def generate_form_details(actor: Actor, *, custom_details: dict = None) -> dict:
    result = {"country": True}

    if custom_details:
        result.update(custom_details)
    return result


def fill_out(driver: WebDriver, details: dict):
    fill_out_input_fields(driver, SELECTORS["form"], details)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])


def get_form_details(driver: WebDriver) -> dict:
    selected_country = find_element(driver, SELECTORS["form"]["country"])
    result = {"country": selected_country.get_attribute("value")}
    return result
