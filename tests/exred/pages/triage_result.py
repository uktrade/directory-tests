# -*- coding: utf-8 -*-
"""ExRed Triage 4th Question Page Object."""
import logging

from selenium import webdriver

from utils import assertion_msg, get_absolute_url, take_screenshot

NAME = "ExRed Triage - result"
URL = get_absolute_url(NAME)

CLASSIFICATION = ".question > h2"
ANSWERS = "div.answers"
CONTINUE_BUTTON = "a.next"
CHANGE_ANSWERS_LINK = "a.update"
BACK_TO_HOME_LINK = "#content > .questions .home-link > a"

EXPECTED_ELEMENTS = {
    "classification": CLASSIFICATION,
    "answers section": ANSWERS,
    "continue button": CONTINUE_BUTTON,
    "change answers link": CHANGE_ANSWERS_LINK,
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


def get_classification(driver: webdriver) -> str:
    element = driver.find_element_by_css_selector(CLASSIFICATION)
    return element.text


def should_be_classified_as(driver: webdriver, expected: str):
    classified = get_classification(driver)
    with assertion_msg(
            "Expected to be classified as '%s' but was classified as: '%s'",
            expected, classified):
        assert classified == expected


def should_be_classified_as_new(driver: webdriver):
    should_be_classified_as(driver, "New to exporting")


def should_be_classified_as_occasional(driver: webdriver):
    should_be_classified_as(driver, "Occasional Exporter")


def should_be_classified_as_regular(driver: webdriver):
    should_be_classified_as(driver, "Regular Exporter")


def create_exporting_journey(driver: webdriver):
    button = driver.find_element_by_css_selector(CONTINUE_BUTTON)
    button.click()
    take_screenshot(driver, NAME + " after submitting")
