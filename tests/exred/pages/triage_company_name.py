# -*- coding: utf-8 -*-
"""Triage - What is your company name? Page Object."""
import random
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import (
    check_for_expected_elements,
    check_title,
    check_url
)
from settings import EXRED_UI_URL
from utils import (
    assertion_msg,
    find_element,
    take_screenshot,
    wait_for_page_load_after_action
)

NAME = "ExRed Triage - What is your company name"
URL = urljoin(EXRED_UI_URL, "triage/company/")
PAGE_TITLE = "Welcome to great.gov.uk"

QUESTION = "label[for=js-typeahead-company-name]"
COMPANY_NAME_INPUT = "js-typeahead-company-name"
SUGGESTIONS = "ul.SelectiveLookupDisplay"
FIRST_SUGGESTION = "ul.SelectiveLookupDisplay > li:nth-child(1)"
CONTINUE_BUTTON = ".exred-triage-form button.button"
PREVIOUS_STEP_BUTTON = "button[name=wizard_goto_step]"
CONTINUE_WO_NAME_BUTTON = "button[name=wizard_skip_step]"
EXPECTED_ELEMENTS = {
    "question": "label[for=js-typeahead-company-name]",
    "continue button": CONTINUE_BUTTON,
    "previous step button": PREVIOUS_STEP_BUTTON,
    "continue without providing name": CONTINUE_WO_NAME_BUTTON,
}


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    check_title(driver, PAGE_TITLE, exact_match=False)
    check_for_expected_elements(driver, EXPECTED_ELEMENTS)


def hide_suggestions(driver: webdriver):
    suggestions = find_element(
        driver, by_css=SUGGESTIONS, element_name="Suggestions list",
        wait_for_it=True)
    if suggestions.is_displayed():
        question = find_element(
            driver, by_css=QUESTION, element_name="Question text",
            wait_for_it=False)
        question.click()


def click_on_first_suggestion(driver: webdriver):
    suggestions = find_element(
        driver, by_css=SUGGESTIONS, element_name="Suggestions",
        wait_for_it=True)
    if suggestions.is_displayed():
        first_suggestion = find_element(
            driver, by_css=FIRST_SUGGESTION, element_name="First suggestion")
        first_suggestion.click()


def enter_company_name(driver: webdriver, company_name: str = None):
    if not company_name:
        company_name = random.choice(["automated", "browser", "tests"])
    input_field = find_element(
        driver, by_id=COMPANY_NAME_INPUT, element_name="Company name input",
        wait_for_it=False)
    input_field.clear()
    input_field.send_keys(company_name)
    take_screenshot(driver, NAME + " after typing in company name")


def get_company_name(driver: webdriver) -> str:
    input_field = find_element(
        driver, by_id=COMPANY_NAME_INPUT, element_name="Company name input",
        wait_for_it=False)
    return input_field.get_attribute("value")


def submit(driver: webdriver):
    button = find_element(
        driver, by_css=CONTINUE_BUTTON, element_name="Continue button",
        wait_for_it=False)
    with wait_for_page_load_after_action(driver):
        button.click()
    take_screenshot(driver, NAME + " after submitting")


def is_company_name(driver: webdriver, company_name: str):
    given = get_company_name(driver)
    with assertion_msg(
            "Expected the company name input box to be prepopulated with: '%s'"
            " but got '%s' instead", company_name, given):
        assert given.lower() == company_name.lower()
