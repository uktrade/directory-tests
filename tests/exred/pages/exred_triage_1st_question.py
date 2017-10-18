# -*- coding: utf-8 -*-
"""ExRed Triage 1st Question Page Object."""
import logging

from tests import get_absolute_url
from tests.exred.drivers import DRIVERS
from tests.exred.utils import take_screenshot
from tests.functional.utils.generic import assertion_msg

URL = get_absolute_url("exred:triage-1st-question")
NAME = "ExRed Triage - 1st question"


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
