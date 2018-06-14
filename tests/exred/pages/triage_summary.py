# -*- coding: utf-8 -*-
"""Triage - Result Page Object."""
from urllib.parse import urljoin

from selenium import webdriver
from utils import (
    assertion_msg,
    check_if_element_is_visible,
    find_element,
    find_elements,
    take_screenshot,
    wait_for_page_load_after_action,
)

from pages.common_actions import (
    check_for_expected_elements,
    check_title,
    check_url,
)
from settings import EXRED_UI_URL

NAME = "ExRed Triage - summary"
URL = urljoin(EXRED_UI_URL, "triage/summary/")
PAGE_TITLE = "Welcome to great.gov.uk"

CLASSIFICATION = "#triage-classification"
ANSWERS_SECTION = "#triage-answers"
CREATE_MY_JOURNEY_BUTTON = "#triage-create-my-export-journey"
PREVIOUS_STEP_BUTTON = "#triage-previous-step"
CHANGE_ANSWERS_LINK = "#triage-change-your-answers"
QUESTIONS = "#triage-answers dt"
ANSWERS = "#triage-answers dd"
EXPECTED_ELEMENTS = {
    "classification": CLASSIFICATION,
    "answers section": ANSWERS_SECTION,
    "continue button": CREATE_MY_JOURNEY_BUTTON,
    "change answers link": CHANGE_ANSWERS_LINK,
}


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    check_title(driver, PAGE_TITLE, exact_match=False)
    check_for_expected_elements(driver, EXPECTED_ELEMENTS)


def get_classification(driver: webdriver) -> str:
    element = find_element(
        driver, by_css=CLASSIFICATION, element_name="Exporter classification"
    )
    return element.text.lower()


def should_be_classified_as(driver: webdriver, expected: str):
    classified = get_classification(driver)
    with assertion_msg(
        "Expected to be classified as '%s' but was classified as: '%s'",
        expected,
        classified,
    ):
        assert classified == expected


def should_be_classified_as_new(driver: webdriver):
    should_be_classified_as(driver, "new exporter")


def should_be_classified_as_occasional(driver: webdriver):
    should_be_classified_as(driver, "occasional exporter")


def should_be_classified_as_regular(driver: webdriver):
    should_be_classified_as(driver, "regular exporter")


def create_exporting_journey(driver: webdriver):
    element_name = "Create my journey button"
    button = find_element(
        driver,
        by_css=CREATE_MY_JOURNEY_BUTTON,
        element_name=element_name,
        wait_for_it=False,
    )
    check_if_element_is_visible(button, element_name=element_name)
    with wait_for_page_load_after_action(driver):
        button.click()
    take_screenshot(driver, NAME + " after submitting")


def get_questions_and_answers(driver: webdriver) -> dict:
    questions = find_elements(driver, by_css=QUESTIONS)
    answers = find_elements(driver, by_css=ANSWERS)
    result = {}
    for q, a in list(zip(questions, answers)):
        result.update({q.text: a.text})
    return result


def change_answers(driver: webdriver):
    link = find_element(
        driver, by_css=CHANGE_ANSWERS_LINK, element_name="Change answers link"
    )
    with wait_for_page_load_after_action(driver):
        link.click()
    take_screenshot(driver, NAME + " after deciding to change the answers")


def should_see_change_your_answers_link(driver: webdriver):
    take_screenshot(driver, NAME + " change your answers")
    change_answers_link = find_element(driver, by_css=CHANGE_ANSWERS_LINK)
    with assertion_msg("Expected to see 'Change your answers' link"):
        assert change_answers_link.is_displayed()
