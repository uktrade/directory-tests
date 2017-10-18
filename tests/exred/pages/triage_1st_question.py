# -*- coding: utf-8 -*-
"""ExRed Triage 1st Question Page Object."""
import logging

from settings import DRIVERS
from utils import assertion_msg, get_absolute_url, take_screenshot

NAME = "ExRed Triage - 1st question"
URL = get_absolute_url(NAME)


SECTOR_OPTIONS = "#q0 > option"
EXPECTED_ELEMENTS = {
    "form legend": "#content > .questions form > fieldset > legend",
    "1st question label": "#content > .questions form > fieldset > label",
    "1st question": "#content > .questions form > fieldset > #q0",
    "continue button":
        "#content > .questions form > fieldset > button[type=submit]",
    "back to home link": "#content > .questions .home-link > a"
}


def visit(driver: DRIVERS, *, first_time: bool = False):
    if first_time:
        logging.debug(
            "Deleting all cookies in order to enforce the first time visit "
            "simulation")
        driver.delete_all_cookies()
    driver.get(URL)
    take_screenshot(driver, NAME)


def should_be_here(driver: DRIVERS):
    for element_name, element_selector in EXPECTED_ELEMENTS.items():
        element = driver.find_element_by_css_selector(element_selector)
        with assertion_msg(
                "It looks like '%s' element is not visible on %s",
                element_name, NAME):
            assert element.is_displayed()
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def extract_sectors(driver: DRIVERS) -> list:
    """Extract all Sector options.

    :param driver: Any Selenium Driver (Remote, Chrome, Firefox, PhantomJS etc.
    :return: a list of available Sectors
    """
    options = driver.find_elements_by_css_selector(SECTOR_OPTIONS)
    option_values = []
    for option in options:
        option_values.append(option.get_attribute("value"))
    return option_values
