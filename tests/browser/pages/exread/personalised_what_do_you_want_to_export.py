# -*- coding: utf-8 -*-
"""Triage - What do you want to export? Page Object."""
import random
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import (
    assertion_msg,
    check_for_expected_elements,
    check_title,
    check_url,
    find_element,
    go_to_url,
    take_screenshot,
    wait_for_page_load_after_action,
)
from settings import EXRED_SECTORS, EXRED_UI_URL

NAME = "ExRed Triage - what do you want to export"
URL = urljoin(EXRED_UI_URL, "triage/sector/")
PAGE_TITLE = "Welcome to great.gov.uk"

SECTORS_COMBOBOX = ".exred-triage-form div[role=combobox]"
SECTORS_INPUT = "#js-sector-select"
AUTOCOMPLETE_1ST_OPTION = "#js-sector-select__option--0"
CONTINUE_BUTTON = "#content .exred-triage-form button[type=submit]"
BACK_TO_HOME_LINK = "#content .home-link a"
EXPECTED_ELEMENTS = {
    "question": "#content .exred-triage-form label",
    "sectors combobox": SECTORS_COMBOBOX,
    "continue button": CONTINUE_BUTTON,
    "back to home link": BACK_TO_HOME_LINK,
}


def visit(driver: webdriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    check_title(driver, PAGE_TITLE, exact_match=False)
    check_for_expected_elements(driver, EXPECTED_ELEMENTS)


def enter(driver: webdriver, code: str, sector: str) -> tuple:
    """Enter information about the things you want to export.

    :param driver: webdriver object
    :param code: sector code. Codes for:
                 Goods start with HS, and for Services with EB (no facts are
                 available for such codes)
    :param sector: specific product to use. Will select random if not set.
    :return: selected code & sector name
    """
    if not code and not sector:
        code, sector = random.choice(list(EXRED_SECTORS.items()))
    input_field = find_element(
        driver,
        by_css=SECTORS_INPUT,
        element_name="Sectors input field",
        wait_for_it=False,
    )
    max_retries = 5
    counter = 0
    while (
        code.lower() not in input_field.get_attribute("value").lower()
    ) and (counter < max_retries):
        input_field.click()
        input_field.clear()
        input_field.send_keys(code or sector)
        counter += 1
    option = find_element(
        driver,
        by_css=AUTOCOMPLETE_1ST_OPTION,
        element_name="Autocomplete list - 1st option",
        wait_for_it=False,
    )
    option.click()
    take_screenshot(driver, NAME)
    return code, sector


def submit(driver: webdriver):
    button = find_element(
        driver,
        by_css=CONTINUE_BUTTON,
        element_name="Continue button",
        wait_for_it=True,
    )
    with wait_for_page_load_after_action(driver):
        button.click()
    take_screenshot(driver, NAME + " after submitting")


def is_sector(driver: webdriver, code: str, sector: str):
    input_field = find_element(
        driver,
        by_css=SECTORS_INPUT,
        element_name="Sector selector",
        wait_for_it=False,
    )
    input_field_value = input_field.get_attribute("value").lower()
    with assertion_msg(
        "Expected the sector input field to be pre-populated with Sector "
        "Code: '%s' but instead found '%s'",
        code,
        input_field_value,
    ):
        assert code.lower() in input_field_value
    with assertion_msg(
        "Expected the sector input field to be pre-populated with Sector "
        "Name: '%s' but instead found '%s'",
        sector,
        input_field_value,
    ):
        assert sector.lower() in input_field_value
