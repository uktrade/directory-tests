# -*- coding: utf-8 -*-
"""Triage  Are you regular exporter? Page Object."""
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import (
    check_for_expected_elements,
    check_title,
    check_url,
)
from settings import EXRED_UI_URL
from utils import (
    assertion_msg,
    find_element,
    take_screenshot,
    wait_for_page_load_after_action,
)

NAME = "ExRed Triage - are you regular exporter"
URL = urljoin(EXRED_UI_URL, "triage/regular-exporter/")
PAGE_TITLE = "Welcome to great.gov.uk"

YES_RADIO = "#triage-regular-exporter-yes"
NO_RADIO = "#triage-regular-exporter-no"
YES_CHECKBOX_LABEL = "#triage-regular-exporter-yes-label"
NO_CHECKBOX_LABEL = "#triage-regular-exporter-no-label"
CONTINUE_BUTTON = "#triage-continue"
PREVIOUS_STEP_BUTTON = "#triage-previous-step"
EXPECTED_ELEMENTS = {
    "question": "#triage-question",
    "yes checkbox label": YES_CHECKBOX_LABEL,
    "no checkbox label": NO_CHECKBOX_LABEL,
    "continue button": CONTINUE_BUTTON,
    "previous step button": PREVIOUS_STEP_BUTTON,
}


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    check_title(driver, PAGE_TITLE, exact_match=False)
    check_for_expected_elements(driver, EXPECTED_ELEMENTS)


def select_yes(driver: webdriver):
    yes = find_element(
        driver,
        by_css=YES_CHECKBOX_LABEL,
        element_name="Yes checkbox",
        wait_for_it=False,
    )
    yes.click()
    take_screenshot(driver, NAME)


def select_no(driver: webdriver):
    no = find_element(
        driver,
        by_css=NO_CHECKBOX_LABEL,
        element_name="No checkbox",
        wait_for_it=False,
    )
    no.click()
    take_screenshot(driver, NAME)


def submit(driver: webdriver):
    button = find_element(
        driver,
        by_css=CONTINUE_BUTTON,
        element_name="Submit button",
        wait_for_it=False,
    )
    with wait_for_page_load_after_action(driver):
        button.click()
    take_screenshot(driver, NAME + " after submitting")


def is_yes_selected(driver: webdriver):
    yes = find_element(
        driver,
        by_css=YES_RADIO,
        element_name="Yes radio button",
        wait_for_it=False,
    )
    with assertion_msg("Expected Yes option to be selected"):
        assert yes.get_property("checked")


def is_no_selected(driver: webdriver):
    no = find_element(
        driver,
        by_css=NO_RADIO,
        element_name="No radio button",
        wait_for_it=False,
    )
    with assertion_msg("Expected No option to be selected"):
        assert no.get_property("checked")
