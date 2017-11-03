# -*- coding: utf-8 -*-
"""Triage - Result Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from settings import EXRED_UI_URL
from utils import assertion_msg, take_screenshot

NAME = "ExRed Triage - result"
URL = urljoin(EXRED_UI_URL, "triage/result")

CLASSIFICATION = ".question > h2"
ANSWERS_SECTION = "div.answers"
CREATE_MY_JOURNEY_BUTTON = "input.button.next"
PREVIOUS_STEP_BUTTON = "input.button.next ~ button.previous-step"
CHANGE_ANSWERS_LINK = "#change-answers-button-container > button"
BACK_TO_HOME_LINK = ".home-link a"
QUESTIONS = ".answers > dl > dt"
ANSWERS = ".answers > dl > dd"
EXPECTED_ELEMENTS = {
    "classification": CLASSIFICATION,
    "answers section": ANSWERS_SECTION,
    "continue button": CREATE_MY_JOURNEY_BUTTON,
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
    return element.text.lower()


def should_be_classified_as(driver: webdriver, expected: str):
    classified = get_classification(driver)
    with assertion_msg(
            "Expected to be classified as '%s' but was classified as: '%s'",
            expected, classified):
        assert classified == expected


def should_be_classified_as_new(driver: webdriver):
    should_be_classified_as(driver, "new exporter")


def should_be_classified_as_occasional(driver: webdriver):
    should_be_classified_as(driver, "occasional exporter")


def should_be_classified_as_regular(driver: webdriver):
    should_be_classified_as(driver, "regular exporter")


def create_exporting_journey(driver: webdriver):
    button = driver.find_element_by_css_selector(CREATE_MY_JOURNEY_BUTTON)
    assert button.is_displayed()
    button.click()
    take_screenshot(driver, NAME + " after submitting")


def get_questions_and_answers(driver: webdriver) -> dict:
    questions = driver.find_elements_by_css_selector(QUESTIONS)
    answers = driver.find_elements_by_css_selector(ANSWERS)
    result = {}
    for q, a in list(zip(questions, answers)):
        result.update({q.text: a.text})
    return result
