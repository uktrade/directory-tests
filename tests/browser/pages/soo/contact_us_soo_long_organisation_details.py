# -*- coding: utf-8 -*-
"""Export Readiness - First page of Long SOO Contact us form"""
import logging
import random
from types import ModuleType
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Actor,
    Selector,
    check_random_radio,
    check_url,
    fill_out_input_fields,
    find_element,
    go_to_url,
    pick_option,
    take_screenshot,
    tick_captcha_checkbox,
    tick_checkboxes,
)
from pages.soo import contact_us_soo_long_your_experience
from settings import SELLING_ONLINE_OVERSEAS_UI_URL

NAME = "Long Domestic (Organisation details)"
SERVICE = "Selling Online Overseas"
TYPE = "Contact us"
URL = urljoin(SELLING_ONLINE_OVERSEAS_UI_URL, "contact/selling-online-overseas/organisation-details/")
PAGE_TITLE = "Welcome to great.gov.uk"

SUBMIT_BUTTON = Selector(
    By.CSS_SELECTOR, "form button[type=submit]", type=ElementType.BUTTON
)
SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#content form"),
        "under £100,000": Selector(
            By.ID, "id_organisation-details-turnover_0", type=ElementType.RADIO,
            group_id=1,
        ),
        "£100,000 to £500,000": Selector(
            By.ID, "id_organisation-details-turnover_1", type=ElementType.RADIO,
            group_id=1,

        ),
        "£500,001 to £2million": Selector(
            By.ID, "id_organisation-details-turnover_2", type=ElementType.RADIO,
            group_id=1,

        ),
        "more than £2million": Selector(
            By.ID, "id_organisation-details-turnover_3", type=ElementType.RADIO,
            group_id=1,

        ),
        "sku": Selector(
            By.ID, "id_organisation-details-sku_count", type=ElementType.INPUT
        ),
        "yes": Selector(
            By.ID, "id_organisation-details-trademarked_0", type=ElementType.RADIO,
            group_id=2,

        ),
        "no": Selector(
            By.ID, "id_organisation-details-trademarked_1", type=ElementType.RADIO,
            group_id=2,

        ),
    }
}

OTHER_SELECTORS = {
    "postcode": Selector(
        By.ID, "id_organisation-company_postcode", type=ElementType.INPUT
    ),
}


def visit(driver: WebDriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL)


def generate_form_details(actor: Actor) -> dict:
    result = {
        "sku": random.randint(0, 10000)
    }
    logging.debug(f"Generated form details: {result}")
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    check_random_radio(driver, form_selectors)
    fill_out_input_fields(driver, form_selectors, details)
    take_screenshot(driver, "After filling out the form")


def submit(driver: WebDriver) -> ModuleType:
    take_screenshot(driver, "Before submitting the form")
    button = find_element(
        driver, SUBMIT_BUTTON, element_name="Submit button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, "After submitting the form")
    return contact_us_soo_long_your_experience
