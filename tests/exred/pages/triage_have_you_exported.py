# -*- coding: utf-8 -*-
"""Triage - Have you exported before? Page Object."""
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

NAME = "ExRed Triage - have you exported before"
URL = urljoin(EXRED_UI_URL, "triage/exported-before/")
PAGE_TITLE = "Welcome to great.gov.uk"

YES_RADIO = "#id_exported-before-exported_before_0"
NO_RADIO = "#id_exported-before-exported_before_1"
YES_CHECKBOX = "#id_exported-before-exported_before > li:nth-child(1) > label"
NO_CHECKBOX = "#id_exported-before-exported_before > li:nth-child(2) > label"
CONTINUE_BUTTON = ".exred-triage-form button.button"
PREVIOUS_STEP_BUTTON = ".exred-triage-form button.previous-step"
BACK_TO_HOME_LINK = ".home-link a"
EXPECTED_ELEMENTS = {
    "question": "#id_triage_wizard_form_view-current_step ~ li > label",
    "yes checkbox": YES_CHECKBOX,
    "no checkbox": NO_CHECKBOX,
    "continue button": CONTINUE_BUTTON,
    "previous step button": PREVIOUS_STEP_BUTTON,
    "back to home link": BACK_TO_HOME_LINK
}


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    check_title(driver, PAGE_TITLE, exact_match=False)
    check_for_expected_elements(driver, EXPECTED_ELEMENTS)


def select_yes(driver: webdriver):
    yes = find_element(
        driver, by_css=YES_CHECKBOX, element_name="YES checkbox",
        wait_for_it=False)
    yes.click()
    take_screenshot(driver, NAME)


def select_no(driver: webdriver):
    no = find_element(
        driver, by_css=NO_CHECKBOX, element_name="NO checkbox",
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
        driver, by_css=YES_RADIO, element_name="Yes checkbox",
        wait_for_it=False)
    with assertion_msg("Expected Yes option to be selected"):
        assert yes.get_property("checked")


def is_no_selected(driver: webdriver):
    no = find_element(
        driver, by_css=NO_RADIO, element_name="No checkbox", wait_for_it=False)
    with assertion_msg("Expected No option to be selected"):
        assert no.get_property("checked")
