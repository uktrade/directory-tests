# -*- coding: utf-8 -*-
"""ExRed Triage 2nd Question Page Object."""
import logging

from settings import DRIVERS
from utils import assertion_msg, get_absolute_url, take_screenshot

NAME = "ExRed Triage - 2nd question"
URL = get_absolute_url(NAME)

YES_CHECKBOX = "#q1-yes ~ label"
NO_CHECKBOX = "#q1-no ~ label"
CONTINUE_BUTTON = ".question form .button"
BACK_TO_HOME_LINK = "#content > .questions .home-link > a"
EXPECTED_ELEMENTS = {
    "question legend": "form > fieldset > legend",
    "question": ".input-container > legend",
    "yes checkbox": YES_CHECKBOX,
    "no checkbox": NO_CHECKBOX,
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


def select_yes(driver: DRIVERS):
    yes = driver.find_element_by_css_selector(YES_CHECKBOX)
    yes.click()
    take_screenshot(driver, NAME)


def select_no(driver: DRIVERS):
    no = driver.find_element_by_css_selector(NO_CHECKBOX)
    no.click()
    take_screenshot(driver, NAME)


def submit(driver: DRIVERS):
    button = driver.find_element_by_css_selector(CONTINUE_BUTTON)
    button.click()
    take_screenshot(driver, NAME + " after submitting")
