# -*- coding: utf-8 -*-
"""Triage - Result Page Object."""
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    assertion_msg,
    check_for_expected_elements,
    check_for_expected_sections_elements,
    check_if_element_is_visible,
    check_title,
    check_url,
    find_element,
    find_elements,
    take_screenshot,
    wait_for_page_load_after_action,
)
from settings import EXRED_UI_URL

NAME = "Triage summary"
SERVICE = "Export Readiness"
TYPE = "triage"
URL = urljoin(EXRED_UI_URL, "triage/summary/")
PAGE_TITLE = "Welcome to great.gov.uk"

CLASSIFICATION = Selector(By.ID, "triage-classification")
ANSWERS_SECTION = Selector(By.ID, "triage-answers")
CREATE_MY_JOURNEY_BUTTON = Selector(By.ID, "triage-create-my-export-journey")
PREVIOUS_STEP_BUTTON = Selector(By.ID, "triage-previous-step")
CHANGE_ANSWERS_LINK = Selector(By.ID, "triage-change-your-answers")
QUESTIONS = Selector(By.CSS_SELECTOR, "#triage-answers dt")
ANSWERS = Selector(By.CSS_SELECTOR, "#triage-answers dd")
SELECTORS = {
    "general": {
        "classification": CLASSIFICATION,
        "answers section": ANSWERS_SECTION,
        "continue button": CREATE_MY_JOURNEY_BUTTON,
        "change answers link": CHANGE_ANSWERS_LINK,
    }
}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    check_title(driver, PAGE_TITLE, exact_match=False)
    check_for_expected_sections_elements(driver, SELECTORS)


def get_classification(driver: WebDriver) -> str:
    element = find_element(
        driver, CLASSIFICATION, element_name="Exporter classification"
    )
    return element.text.lower()


def should_be_classified_as(driver: WebDriver, expected: str):
    classified = get_classification(driver)
    with assertion_msg(
        "Expected to be classified as '%s' but was classified as: '%s'",
        expected,
        classified,
    ):
        assert classified == expected


def should_be_classified_as_new(driver: WebDriver):
    should_be_classified_as(driver, "new exporter")


def should_be_classified_as_occasional(driver: WebDriver):
    should_be_classified_as(driver, "occasional exporter")


def should_be_classified_as_regular(driver: WebDriver):
    should_be_classified_as(driver, "regular exporter")


def create_exporting_journey(driver: WebDriver):
    element_name = "Create my journey button"
    button = find_element(
        driver, CREATE_MY_JOURNEY_BUTTON, element_name=element_name, wait_for_it=False
    )
    check_if_element_is_visible(button, element_name=element_name)
    with wait_for_page_load_after_action(driver):
        button.click()
    take_screenshot(driver, NAME + " after submitting")


def get_questions_and_answers(driver: WebDriver) -> dict:
    questions = find_elements(driver, QUESTIONS)
    answers = find_elements(driver, ANSWERS)
    result = {}
    for q, a in list(zip(questions, answers)):
        result.update({q.text: a.text})
    return result


def change_answers(driver: WebDriver):
    link = find_element(driver, CHANGE_ANSWERS_LINK, element_name="Change answers link")
    with wait_for_page_load_after_action(driver):
        link.click()
    take_screenshot(driver, NAME + " after deciding to change the answers")


def should_see_change_your_answers_link(driver: WebDriver):
    take_screenshot(driver, NAME + " change your answers")
    change_answers_link = find_element(driver, CHANGE_ANSWERS_LINK)
    with assertion_msg("Expected to see 'Change your answers' link"):
        assert change_answers_link.is_displayed()
