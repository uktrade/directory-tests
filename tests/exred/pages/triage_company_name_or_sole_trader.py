# -*- coding: utf-8 -*-
"""ExRed Triage 4th Question Page Object."""
import logging
import random

from selenium import webdriver

from utils import assertion_msg, get_absolute_url, take_screenshot

NAME = "ExRed Triage - 4th question"
URL = get_absolute_url(NAME)

COMPANY_NAME_INPUT = "#js-typeahead-company-name"
SOLE_TRADER_CHECKBOX = ".form-field label[for=id_COMPANY-sole_trader]"
CONTINUE_BUTTON = ".exred-triage-form button.button"
PREVIOUS_STEP_BUTTON = ".exred-triage-form button.previous-step"
BACK_TO_HOME_LINK = ".home-link a"
EXPECTED_ELEMENTS = {
    "question": "label[for=js-typeahead-company-name]",
    "continue button": CONTINUE_BUTTON,
    "previous step button": PREVIOUS_STEP_BUTTON,
    "back to home link": BACK_TO_HOME_LINK
}


def should_be_here(driver: webdriver):
    for element_name, element_selector in EXPECTED_ELEMENTS.items():
        element = driver.find_element_by_css_selector(element_selector)
        with assertion_msg(
                "It looks like '%s' element is not visible on %s",
                element_name, NAME):
            assert element.is_displayed()
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def enter_company_name(driver: webdriver, *, company_name: str = None):
    if not company_name:
        company_name = "Random company {}".format(random.randrange(0, 9999999))
    input_field = driver.find_element_by_css_selector(COMPANY_NAME_INPUT)
    input_field.clear()
    input_field.send_keys(company_name)
    take_screenshot(driver, NAME + " after typing in company name")


def select_sole_trade(driver: webdriver):
    sole_trader = driver.find_element_by_css_selector(SOLE_TRADER_CHECKBOX)
    sole_trader.click()
    take_screenshot(driver, NAME + " selected sole trader")


def submit(driver: webdriver):
    button = driver.find_element_by_css_selector(CONTINUE_BUTTON)
    button.click()
    take_screenshot(driver, NAME + " after submitting")
