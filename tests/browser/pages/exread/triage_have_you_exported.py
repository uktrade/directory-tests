# -*- coding: utf-8 -*-
"""Triage - Have you exported before? Page Object."""
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    assertion_msg,
    check_for_expected_elements,
    check_title,
    check_url,
    find_element,
    go_to_url,
    take_screenshot,
    wait_for_page_load_after_action,
    Selector
)
from settings import EXRED_UI_URL

NAME = "Have you exported before"
SERVICE = "Export Readiness"
TYPE = "triage"
URL = urljoin(EXRED_UI_URL, "triage/exported-before/")
PAGE_TITLE = "Welcome to great.gov.uk"

YES_RADIO = Selector(By.ID, "triage-exported-before-yes")
NO_RADIO = Selector(By.ID, "triage-exported-before-no")
YES_CHECKBOX = Selector(By.ID, "triage-exported-before-yes-label")
NO_CHECKBOX = Selector(By.ID, "triage-exported-before-no-label")
CONTINUE_BUTTON = Selector(By.ID, "triage-continue")
BACK_TO_HOME_LINK = Selector(By.ID, "triage-question-back-to-home")
EXPECTED_ELEMENTS = {
    "question": Selector(By.ID, "triage-question"),
    "yes checkbox": YES_CHECKBOX,
    "no checkbox": NO_CHECKBOX,
    "continue button": CONTINUE_BUTTON,
    "back to home link": BACK_TO_HOME_LINK,
}
SELECTORS = {}


def visit(driver: WebDriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    check_title(driver, PAGE_TITLE, exact_match=False)
    check_for_expected_elements(driver, EXPECTED_ELEMENTS)


def select_yes(driver: WebDriver):
    yes = find_element(
        driver, YES_CHECKBOX, element_name="YES checkbox", wait_for_it=False
    )
    yes.click()
    take_screenshot(driver, NAME)


def select_no(driver: WebDriver):
    no = find_element(
        driver, NO_CHECKBOX, element_name="NO checkbox", wait_for_it=False
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
        driver, YES_RADIO, element_name="Yes checkbox", wait_for_it=False
    )
    with assertion_msg("Expected Yes option to be selected"):
        assert yes.get_property("checked")


def is_no_selected(driver: WebDriver):
    no = find_element(
        driver, NO_RADIO, element_name="No checkbox", wait_for_it=False
    )
    with assertion_msg("Expected No option to be selected"):
        assert no.get_property("checked")
