# -*- coding: utf-8 -*-
"""Triage  Are you regular exporter? Page Object."""
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    assertion_msg,
    check_for_expected_elements,
    check_title,
    check_url,
    find_element,
    take_screenshot,
    wait_for_page_load_after_action,
    Selector
)
from settings import EXRED_UI_URL

NAME = "Are you regular exporter"
SERVICE = "Export Readiness"
TYPE = "triage"
URL = urljoin(EXRED_UI_URL, "triage/regular-exporter/")
PAGE_TITLE = "Welcome to great.gov.uk"

YES_RADIO = Selector(By.ID, "triage-regular-exporter-yes")
NO_RADIO = Selector(By.ID, "triage-regular-exporter-no")
YES_CHECKBOX_LABEL = Selector(By.ID, "triage-regular-exporter-yes-label")
NO_CHECKBOX_LABEL = Selector(By.ID, "triage-regular-exporter-no-label")
CONTINUE_BUTTON = Selector(By.ID, "triage-continue")
PREVIOUS_STEP_BUTTON = Selector(By.ID, "triage-previous-step")
EXPECTED_ELEMENTS = {
    "question": Selector(By.ID, "triage-question"),
    "yes checkbox label": YES_CHECKBOX_LABEL,
    "no checkbox label": NO_CHECKBOX_LABEL,
    "continue button": CONTINUE_BUTTON,
    "previous step button": PREVIOUS_STEP_BUTTON,
}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    check_title(driver, PAGE_TITLE, exact_match=False)
    check_for_expected_elements(driver, EXPECTED_ELEMENTS)


def select_yes(driver: WebDriver):
    yes = find_element(
        driver,
        YES_CHECKBOX_LABEL,
        element_name="Yes checkbox",
        wait_for_it=False,
    )
    yes.click()
    take_screenshot(driver, NAME)


def select_no(driver: WebDriver):
    no = find_element(
        driver, NO_CHECKBOX_LABEL, element_name="No checkbox", wait_for_it=False
    )
    no.click()
    take_screenshot(driver, NAME)


def submit(driver: WebDriver):
    button = find_element(
        driver, CONTINUE_BUTTON, element_name="Submit button", wait_for_it=False
    )
    with wait_for_page_load_after_action(driver):
        button.click()
    take_screenshot(driver, NAME + " after submitting")


def is_yes_selected(driver: WebDriver):
    yes = find_element(
        driver, YES_RADIO, element_name="Yes radio button", wait_for_it=False
    )
    with assertion_msg("Expected Yes option to be selected"):
        assert yes.get_property("checked")


def is_no_selected(driver: WebDriver):
    no = find_element(
        driver, NO_RADIO, element_name="No radio button", wait_for_it=False
    )
    with assertion_msg("Expected No option to be selected"):
        assert no.get_property("checked")
