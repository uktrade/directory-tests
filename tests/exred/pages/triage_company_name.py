# -*- coding: utf-8 -*-
"""Triage - What is your company name? Page Object."""
import logging
import random
from urllib.parse import urljoin

from selenium import webdriver

from settings import EXRED_UI_URL
from utils import assertion_msg, take_screenshot

NAME = "ExRed Triage - What is your company name"
URL = urljoin(EXRED_UI_URL, "triage")

COMPANY_NAME_INPUT = "#js-typeahead-company-name"
SUGGESTIONS = "ul.SelectiveLookupDisplay"
FIRST_SUGGESTION = "ul.SelectiveLookupDisplay > li:nth-child(1)"
CONTINUE_BUTTON = ".exred-triage-form button.button"
PREVIOUS_STEP_BUTTON = ".exred-triage-form button.previous-step"
CONTINUE_WO_NAME_BUTTON = "div.exred-triage-form button[name=wizard_skip_step]"
BACK_TO_HOME_LINK = ".home-link a"
EXPECTED_ELEMENTS = {
    "question": "label[for=js-typeahead-company-name]",
    "continue button": CONTINUE_BUTTON,
    "previous step button": PREVIOUS_STEP_BUTTON,
    "continue without providing name": CONTINUE_WO_NAME_BUTTON,
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
        company_name = random.choice(["automated", "browser", "tests"])
    input_field = driver.find_element_by_css_selector(COMPANY_NAME_INPUT)
    input_field.clear()
    input_field.send_keys(company_name)
    suggestions = driver.find_element_by_css_selector(SUGGESTIONS)
    if suggestions.is_displayed():
        first_suggestion = driver.find_element_by_css_selector(FIRST_SUGGESTION)
        first_suggestion.click()
    take_screenshot(driver, NAME + " after typing in company name")


def submit(driver: webdriver):
    button = driver.find_element_by_css_selector(CONTINUE_BUTTON)
    button.click()
    take_screenshot(driver, NAME + " after submitting")
