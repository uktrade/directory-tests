# -*- coding: utf-8 -*-
"""ERP - Country select"""
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
    fill_out_input_fields,
    submit_form,
)
from pages.erp import uk_importer_are_goods_used_to_make_something_else
from pages.erp.autocomplete_callbacks import autocomplete_country

NAME = "Where do you import from (UK importer)"
SERVICE = Service.ERP
TYPE = PageType.FORM
URL = URLs.ERP_IMPORTER_WHICH_COUNTRIES.absolute
PAGE_TITLE = ""

SELECTORS = {
    "form": {
        "form itself": Selector(By.CSS_SELECTOR, "#content form[method='post']"),
        "country": Selector(
            By.ID,
            "id_which-countries-import_countries_autocomplete",
            type=ElementType.INPUT,
            is_visible=False,
            autocomplete_callback=autocomplete_country,
        ),
        "continue": Selector(
            By.CSS_SELECTOR,
            "#content > form button.govuk-button",
            type=ElementType.SUBMIT,
            next_page=uk_importer_are_goods_used_to_make_something_else,
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
    result = {"country": True}

    if custom_details:
        result.update(custom_details)
    return result


def fill_out(driver: WebDriver, details: dict):
    fill_out_input_fields(driver, SELECTORS["form"], details)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
