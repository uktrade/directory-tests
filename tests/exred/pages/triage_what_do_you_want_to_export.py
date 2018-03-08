# -*- coding: utf-8 -*-
"""Triage What do you want to export page."""
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

NAME = "ExRed Triage - What do you want to export"
URL = urljoin(EXRED_UI_URL, "triage/good-or-services/")
PAGE_TITLE = "Welcome to great.gov.uk"

QUESTION_LABEL = "#triage-question-label"
QUESTION = "#triage-question"
SERVICES_CHECKBOX = "#triage-answer-services"
GOODS_CHECKBOX = "#triage-answer-goods"
SERVICES_CHECKBOX_LABEL = "#triage-answer-services-label"
GOODS_CHECKBOX_LABEL = "#triage-answer-goods-label"
CONTINUE_BUTTON = "#triage-continue"
PREVIOUS_STEP_BUTTON = "#triage-previous-step"
BACK_TO_HOME_LINK = "#triage-go-back-home"
SKIP_THIS_STEP_LINK = "#triage-skip-this-step"
EXPECTED_ELEMENTS = {
    "question": "#id_triage_wizard_form_view-current_step ~ li > label",
    "services checkbox": SERVICES_CHECKBOX,
    "goods checkbox": GOODS_CHECKBOX,
    "continue button": CONTINUE_BUTTON,
    "previous step button": PREVIOUS_STEP_BUTTON,
    "back to home link": BACK_TO_HOME_LINK
}


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    check_title(driver, PAGE_TITLE, exact_match=False)
    check_for_expected_elements(driver, EXPECTED_ELEMENTS)


def select_services(driver: webdriver):
    yes = find_element(
        driver, by_css=SERVICES_CHECKBOX, element_name="Services checkbox",
        wait_for_it=False)
    yes.click()
    take_screenshot(driver, NAME)


def select_goods(driver: webdriver):
    no = find_element(
        driver, by_css=GOODS_CHECKBOX, element_name="Goods checkbox",
        wait_for_it=False)
    no.click()
    take_screenshot(driver, NAME)


def submit(driver: webdriver):
    button = find_element(
        driver, by_css=CONTINUE_BUTTON, element_name="Submit button",
        wait_for_it=False)
    with wait_for_page_load_after_action(driver):
        button.click()
    take_screenshot(driver, NAME + " after submitting")


def is_yes_selected(driver: webdriver):
    yes = find_element(
        driver, by_css=SERVICES_CHECKBOX, element_name="Yes radio button",
        wait_for_it=False)
    with assertion_msg("Expected Yes option to be selected"):
        assert yes.get_property("checked")


def is_no_selected(driver: webdriver):
    no = find_element(
        driver, by_css=GOODS_CHECKBOX, element_name="No radio button",
        wait_for_it=False)
    with assertion_msg("Expected No option to be selected"):
        assert no.get_property("checked")
