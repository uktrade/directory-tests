# -*- coding: utf-8 -*-
"""ExRed Triage 1st Question Page Object."""
import logging
import random

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select

from utils import assertion_msg, get_absolute_url, take_screenshot

NAME = "ExRed Triage - 1st question"
URL = get_absolute_url(NAME)

SECTORS_DROPDOWN = "#id_SECTOR-sector"
SECTOR_OPTIONS = "#id_SECTOR-sector option"
CONTINUE_BUTTON = "#content .exred-triage-form button[type=submit]"
BACK_TO_HOME_LINK = "#content .home-link a"
EXPECTED_ELEMENTS = {
    "question": "#content .exred-triage-form label",
    "sectors dropdown": SECTORS_DROPDOWN,
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
        option_values.append(option.get_attribute("value"))
    return option_values


def select_sector(driver: webdriver, sector: str):
    if not sector:
        sector = random.choice(extract_sectors_values(driver))
    options = driver.find_element_by_css_selector(SECTORS_DROPDOWN)
    assert options.is_displayed()
    select = Select(options)
    select.select_by_value(sector)
    take_screenshot(driver, NAME)


def submit(driver: webdriver):
    button = driver.find_element_by_css_selector(CONTINUE_BUTTON)
    assert button.is_displayed()
    actions = ActionChains(driver)
    actions.move_to_element(button)
    actions.click(button)
    actions.perform()
    take_screenshot(driver, NAME + " after submitting")
