# -*- coding: utf-8 -*-
"""Domestic - 3/4 page of Long SOO Contact us form"""
import logging
import random
from types import ModuleType
from typing import Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType, common_selectors
from pages.common_actions import (
    Actor,
    Selector,
    check_random_radio,
    check_url,
    fill_out_input_fields,
    submit_form,
    take_screenshot,
)
from pages.domestic import contact_us_soo_4_your_experience

NAME = "About your products (SOO)"
SERVICE = Service.DOMESTIC
TYPE = PageType.CONTACT_US
URL = URLs.CONTACT_US_SOO_ORGANISATION_CONTACT_APPLICANT_DETAILS.absolute
PAGE_TITLE = "Welcome to great.gov.uk"

SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#content form"),
        "sku": Selector(
            By.ID, "id_applicant-details-sku_count", type=ElementType.INPUT
        ),
        "yes": Selector(
            By.ID,
            "id_applicant-details-trademarked_0",
            type=ElementType.RADIO,
            group_id=1,
        ),
        "no": Selector(
            By.ID,
            "id_applicant-details-trademarked_1",
            type=ElementType.RADIO,
            group_id=1,
        ),
        "submit": Selector(
            By.CSS_SELECTOR,
            "form button.button[type=submit]",
            type=ElementType.SUBMIT,
            next_page=contact_us_soo_4_your_experience,
        ),
    }
}
SELECTORS.update(common_selectors.DOMESTIC_HEADER)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.DOMESTIC_FOOTER)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL)


def generate_form_details(actor: Actor) -> dict:
    result = {"sku": random.randint(0, 10000)}
    logging.debug(f"Generated form details: {result}")
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    check_random_radio(driver, form_selectors)
    fill_out_input_fields(driver, form_selectors, details)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
