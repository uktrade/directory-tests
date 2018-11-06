# -*- coding: utf-8 -*-
"""Triage What do you want to export page."""
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    assertion_msg,
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

QUESTION_LABEL = Selector(By.ID, "triage-question-label")
QUESTION = Selector(By.ID, "triage-question")
SERVICES_CHECKBOX = Selector(By.ID, "triage-services")
SERVICES_CHECKBOX_LABEL = Selector(By.ID, "triage-services-label")
GOODS_CHECKBOX = Selector(By.ID, "triage-goods")
GOODS_CHECKBOX_LABEL = Selector(By.ID, "triage-goods-label")
CONTINUE_BUTTON = Selector(By.ID, "triage-continue")
PREVIOUS_STEP_BUTTON = Selector(By.ID, "triage-previous-step")
SELECTORS = {
    "general": {
        "question": QUESTION,
        "question label": QUESTION_LABEL,
        # "services checkbox": SERVICES_CHECKBOX,
        "services checkbox label": SERVICES_CHECKBOX_LABEL,
        # "goods checkbox": GOODS_CHECKBOX,
        "goods checkbox label": GOODS_CHECKBOX_LABEL,
        "continue button": CONTINUE_BUTTON,
        "previous step button": PREVIOUS_STEP_BUTTON,
    }
}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)


def select_services(driver: WebDriver):
    services = find_element(
        driver, SERVICES_CHECKBOX, element_name="Services checkbox", wait_for_it=False
    )
    services.click()
    take_screenshot(driver, NAME)


def select_goods(driver: WebDriver):
    goods = find_element(
        driver, GOODS_CHECKBOX, element_name="Goods checkbox", wait_for_it=False
    )
    goods.click()
    take_screenshot(driver, NAME)


def select_goods_and_services(driver: WebDriver):
    goods = find_element(
        driver, GOODS_CHECKBOX, element_name="Goods checkbox", wait_for_it=False
    )
    goods.click()
    services = find_element(
        driver, SERVICES_CHECKBOX, element_name="Services checkbox", wait_for_it=False
    )
    services.click()
    take_screenshot(driver, NAME)


def submit(driver: WebDriver):
    submit_button = find_element(
        driver, CONTINUE_BUTTON, element_name="Submit button", wait_for_it=False
    )
    with wait_for_page_load_after_action(driver):
        submit_button.click()
    take_screenshot(driver, NAME + " after submitting")


def is_services_selected(driver: WebDriver):
    services = find_element(
        driver,
        SERVICES_CHECKBOX,
        element_name="Services radio button",
        wait_for_it=False,
    )
    with assertion_msg("Expected Services option to be selected"):
        assert services.get_property("checked")


def is_goods_selected(driver: WebDriver):
    goods = find_element(
        driver, GOODS_CHECKBOX, element_name="Goods radio button", wait_for_it=False
    )
    with assertion_msg("Expected Goods option to be selected"):
        assert goods.get_property("checked")
