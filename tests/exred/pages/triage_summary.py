# -*- coding: utf-8 -*-
"""Triage - Result Page Object."""
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import (
    check_for_expected_elements,
    check_title,
    check_url
)
from settings import EXRED_UI_URL
from utils import assertion_msg, find_element, take_screenshot

NAME = "ExRed Triage - summary"
URL = urljoin(EXRED_UI_URL, "triage/summary/")
PAGE_TITLE = "Welcome to great.gov.uk"

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
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    check_title(driver, PAGE_TITLE, exact_match=False)
    check_for_expected_elements(driver, EXPECTED_ELEMENTS)


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


def change_answers(driver: webdriver):
    link = driver.find_element_by_css_selector(CHANGE_ANSWERS_LINK)
    link.click()
    take_screenshot(driver, NAME + " after deciding to change the answers")


def should_see_change_your_answers_link(driver: webdriver):
    take_screenshot(driver, NAME + " change your answers")
    change_answers_link = find_element(driver, by_css=CHANGE_ANSWERS_LINK)
    with assertion_msg("Expected to see 'Change your answers' link"):
        assert change_answers_link.is_displayed()
