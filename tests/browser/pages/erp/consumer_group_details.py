# -*- coding: utf-8 -*-
"""ERP - Consumer group details - UK consumer"""
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
    find_element,
    find_elements,
    find_selector_by_name,
    submit_form,
)
from pages.erp import summary
from pages.erp.autocomplete_callbacks import autocomplete_uk_region

NAME = "Consumer group details (UK consumer)"
SERVICE = Service.ERP
TYPE = PageType.FORM
URL = URLs.ERP_CONSUMER_GROUP_DETAILS.absolute
PAGE_TITLE = ""


SELECTORS = {
    "form": {
        "selection form": Selector(By.CSS_SELECTOR, "#content form[method='post']"),
        "step counter": Selector(
            By.CSS_SELECTOR, "form[method=post] span.govuk-caption-l"
        ),
        "heading": Selector(By.CSS_SELECTOR, "form[method=post] h1"),
        "given name": Selector(
            By.ID, "id_consumer-group-given_name", type=ElementType.INPUT
        ),
        "family name": Selector(
            By.ID, "id_consumer-group-family_name", type=ElementType.INPUT
        ),
        "email": Selector(By.ID, "id_consumer-group-email", type=ElementType.INPUT),
        "organisation name": Selector(
            By.ID, "id_consumer-group-organisation_name", type=ElementType.INPUT
        ),
        "regions": Selector(
            By.ID,
            "id_consumer-group-consumer_regions_autocomplete",
            type=ElementType.INPUT,
            autocomplete_callback=autocomplete_uk_region,
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

SELECTED_REGIONS = Selector(
    By.CSS_SELECTOR,
    "span.multi-select-autocomplete-selected-item button",
    type=ElementType.BUTTON,
)


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=False)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def generate_form_details(actor: Actor, *, custom_details: dict = None) -> dict:
    result = {
        "given name": actor.alias,
        "family name": str(uuid4()),
        "email": actor.email,
        "organisation name": "AUTOMATED TESTS",
        "regions": True,
    }
    if custom_details:
        result.update(custom_details)
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    fill_out_input_fields(driver, form_selectors, details)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])


def get_form_details(driver: WebDriver) -> dict:
    elements = find_elements(driver, SELECTED_REGIONS)
    result = {"regions": []}
    for element in elements:
        region_name = element.get_property("value")
        result["regions"].append(region_name)
    result["organisation name"] = "AUTOMATED TESTS"
    result["given mane"] = find_element(
        driver, find_selector_by_name(SELECTORS, "given name")
    ).get_property("value")
    result["family mane"] = find_element(
        driver, find_selector_by_name(SELECTORS, "family name")
    ).get_property("value")
    result["email"] = find_element(
        driver, find_selector_by_name(SELECTORS, "email")
    ).get_property("value")
    return result
