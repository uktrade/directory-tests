# -*- coding: utf-8 -*-
"""Triage What do you want to export page."""
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import (
    assertion_msg,
    check_for_expected_elements,
    check_title,
    check_url,
    find_element,
    take_screenshot,
    wait_for_page_load_after_action,
)
from settings import EXRED_UI_URL

NAME = "What do you want to export"
SERVICE = "Export Readiness"
TYPE = "triage"
URL = urljoin(EXRED_UI_URL, "triage/goods-services/")
PAGE_TITLE = "Welcome to great.gov.uk"

QUESTION_LABEL = "#triage-question-label"
QUESTION = "#triage-question"
SERVICES_CHECKBOX = "#triage-services"
SERVICES_CHECKBOX_LABEL = "#triage-services-label"
GOODS_CHECKBOX = "#triage-goods"
GOODS_CHECKBOX_LABEL = "#triage-goods-label"
CONTINUE_BUTTON = "#triage-continue"
PREVIOUS_STEP_BUTTON = "#triage-previous-step"
EXPECTED_ELEMENTS = {
    "question": QUESTION,
    "question label": QUESTION_LABEL,
    # "services checkbox": SERVICES_CHECKBOX,
    "services checkbox label": SERVICES_CHECKBOX_LABEL,
    # "goods checkbox": GOODS_CHECKBOX,
    "goods checkbox label": GOODS_CHECKBOX_LABEL,
    "continue button": CONTINUE_BUTTON,
    "previous step button": PREVIOUS_STEP_BUTTON,
}
SELECTORS = {}


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    check_title(driver, PAGE_TITLE, exact_match=False)
    check_for_expected_elements(driver, EXPECTED_ELEMENTS)


def select_services(driver: webdriver):
    services = find_element(
        driver,
        by_css=SERVICES_CHECKBOX,
        element_name="Services checkbox",
        wait_for_it=False,
    )
    services.click()
    take_screenshot(driver, NAME)


def select_goods(driver: webdriver):
    goods = find_element(
        driver, by_css=GOODS_CHECKBOX, element_name="Goods checkbox", wait_for_it=False
    )
    goods.click()
    take_screenshot(driver, NAME)


def select_goods_and_services(driver: webdriver):
    goods = find_element(
        driver, by_css=GOODS_CHECKBOX, element_name="Goods checkbox", wait_for_it=False
    )
    goods.click()
    services = find_element(
        driver,
        by_css=SERVICES_CHECKBOX,
        element_name="Services checkbox",
        wait_for_it=False,
    )
    services.click()
    take_screenshot(driver, NAME)


def submit(driver: webdriver):
    submit_button = find_element(
        driver, by_css=CONTINUE_BUTTON, element_name="Submit button", wait_for_it=False
    )
    with wait_for_page_load_after_action(driver):
        submit_button.click()
    take_screenshot(driver, NAME + " after submitting")


def is_services_selected(driver: webdriver):
    services = find_element(
        driver,
        by_css=SERVICES_CHECKBOX,
        element_name="Services radio button",
        wait_for_it=False,
    )
    with assertion_msg("Expected Services option to be selected"):
        assert services.get_property("checked")


def is_goods_selected(driver: webdriver):
    goods = find_element(
        driver,
        by_css=GOODS_CHECKBOX,
        element_name="Goods radio button",
        wait_for_it=False,
    )
    with assertion_msg("Expected Goods option to be selected"):
        assert goods.get_property("checked")
