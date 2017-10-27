# -*- coding: utf-8 -*-
"""Triage - What is you sector? Page Object."""
import logging
import random
from urllib.parse import urljoin

from selenium import webdriver

from settings import EXRED_SECTORS, EXRED_UI_URL
from utils import assertion_msg, selenium_action, take_screenshot

NAME = "ExRed Triage - what is your sector"
URL = urljoin(EXRED_UI_URL, "triage")

SECTORS_COMBOBOX = ".exred-triage-form div[role=combobox]"
SECTORS_INPUT = "#js-sector-select"
AUTOCOMPLETE_1ST_OPTION = "#js-sector-select__option--0"
CONTINUE_BUTTON = "#content .exred-triage-form button[type=submit]"
BACK_TO_HOME_LINK = "#content .home-link a"
EXPECTED_ELEMENTS = {
    "question": "#content .exred-triage-form label",
    "sectors combobox": SECTORS_COMBOBOX,
    "continue button": CONTINUE_BUTTON,
    "back to home link": BACK_TO_HOME_LINK
}


def visit(driver: webdriver, *, first_time: bool = False):
    if first_time:
        logging.debug(
            "Deleting all cookies in order to enforce the first time visit "
            "simulation")
        driver.delete_all_cookies()
    driver.get(URL)
    take_screenshot(driver, NAME)


def should_be_here(driver: webdriver):
    for element_name, element_selector in EXPECTED_ELEMENTS.items():
        element = driver.find_element_by_css_selector(element_selector)
        with assertion_msg(
                "It looks like '%s' element is not visible on %s",
                element_name, NAME):
            assert element.is_displayed()
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def select_sector(driver: webdriver, sector: str):
    if not sector:
        sector = random.choice(list(EXRED_SECTORS.values()))
    with selenium_action(driver, "Can't find Sector selector input box"):
        input_field = driver.find_element_by_css_selector(SECTORS_INPUT)
    input_field.click()
    input_field.clear()
    input_field.send_keys(sector)
    with selenium_action(driver, "Can't find Autocomplete 1st option"):
        option = driver.find_element_by_css_selector(AUTOCOMPLETE_1ST_OPTION)
    option.click()
    take_screenshot(driver, NAME)


def submit(driver: webdriver):
    button = driver.find_element_by_css_selector(CONTINUE_BUTTON)
    assert button.is_displayed()
    button.click()
    take_screenshot(driver, NAME + " after submitting")
