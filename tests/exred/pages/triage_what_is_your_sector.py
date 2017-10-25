# -*- coding: utf-8 -*-
"""ExRed Triage 1st Question Page Object."""
import logging
import random
from urllib.parse import urljoin

from selenium import webdriver

from settings import EXRED_UI_URL
from utils import assertion_msg, selenium_action, take_screenshot

NAME = "ExRed Triage - what is your sector"
URL = urljoin(EXRED_UI_URL, "triage")

SECTORS_COMBOBOX = ".exred-triage-form div[role=combobox]"
SECTORS_INPUT = "#js-sector-select"
SECTORS_SELECT_LIST = "js-sector-select-select"
SECTOR_OPTIONS = "#js-sector-select-select > option"
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


def extract_sectors_values(driver: webdriver) -> list:
    """Extract all Sector options.

    :param driver: Any Selenium Driver (Remote, Chrome, Firefox, PhantomJS etc.
    :return: a list of available Sectors
    """
    options = driver.find_elements_by_css_selector(SECTOR_OPTIONS)
    option_values = []
    for option in options:
        text = option.get_attribute("text")
        if text != "---------":
            option_values.append(text)
    return option_values


def select_sector(driver: webdriver, sector: str):
    if not sector:
        sector = random.choice(extract_sectors_values(driver))
    with selenium_action(driver, "Can't find Sector selector input box"):
        input = driver.find_element_by_css_selector(SECTORS_INPUT)
    input.click()
    input.clear()
    input.send_keys(sector)
    with selenium_action(driver, "Can't find Autocomplete 1st option"):
        option = driver.find_element_by_css_selector(AUTOCOMPLETE_1ST_OPTION)
    option.click()
    take_screenshot(driver, NAME)


def submit(driver: webdriver):
    button = driver.find_element_by_css_selector(CONTINUE_BUTTON)
    assert button.is_displayed()
    button.click()
    take_screenshot(driver, NAME + " after submitting")
