# -*- coding: utf-8 -*-
"""ExRed Triage 4th Question Page Object."""
import logging
import random

from settings import DRIVERS
from utils import assertion_msg, get_absolute_url, take_screenshot

NAME = "ExRed Triage - 4th question"
URL = get_absolute_url(NAME)

CONTINUE_BUTTON = ".question form .button"
BACK_TO_HOME_LINK = "#content > .questions .home-link > a"
COMPANY_NAME_INPUT = "#q3_a"
SOLE_TRADER_CHECKBOX = "#q3_b ~ label"
EXPECTED_ELEMENTS = {
    "question legend": ".question > form fieldset legend",
    "question": ".question > form fieldset legend ~ label",
    "continue button": CONTINUE_BUTTON,
    "back to home link": BACK_TO_HOME_LINK
}


def should_be_here(driver: DRIVERS):
    for element_name, element_selector in EXPECTED_ELEMENTS.items():
        element = driver.find_element_by_css_selector(element_selector)
        with assertion_msg(
                "It looks like '%s' element is not visible on %s",
                element_name, NAME):
            assert element.is_displayed()
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def enter_company_name(driver: DRIVERS, *, company_name: str = None):
    if not company_name:
        company_name = "Random company {}".format(random.randrange(0, 9999999))
    input_field = driver.find_element_by_css_selector(COMPANY_NAME_INPUT)
    input_field.send_keys(company_name)
    take_screenshot(driver, NAME + " after typing in company name")


def select_sole_trade(driver: DRIVERS):
    sole_trader = driver.find_element_by_css_selector(SOLE_TRADER_CHECKBOX)
    sole_trader.click()
    take_screenshot(driver, NAME + " selected sole trader")


def submit(driver: DRIVERS):
    button = driver.find_element_by_css_selector(CONTINUE_BUTTON)
    button.click()
    take_screenshot(driver, NAME + " after submitting")
