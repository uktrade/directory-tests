# -*- coding: utf-8 -*-
"""Export Readiness - Domestic Contact us - Great.gov.uk account"""
import logging
from types import ModuleType
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Selector,
    check_url,
    choose_one_form_option,
    choose_one_form_option_except,
    find_and_click_on_page_element,
    find_element,
    get_selectors,
    go_to_url,
    take_screenshot,
)
from pages.exread import (
    contact_us_short_domestic,
    contact_us_triage_great_account_dedicated_support_content,
)
from settings import EXRED_UI_URL

NAME = "Great.gov.uk account"
SERVICE = "Export Readiness"
TYPE = "Domestic Contact us"
URL = urljoin(EXRED_UI_URL, "contact/triage/great-account/")
PAGE_TITLE = "Welcome to great.gov.uk"

SUBMIT_BUTTON = Selector(
    By.CSS_SELECTOR, "form button[type=submit]", type=ElementType.BUTTON
)
SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#lede form"),
        "i have not received an email confirmation": Selector(
            By.ID, "id_great-account-choice_0", type=ElementType.RADIO, is_visible=False
        ),
        "i need to reset my password": Selector(
            By.ID, "id_great-account-choice_1", type=ElementType.RADIO, is_visible=False
        ),
        "my companies house login is not working": Selector(
            By.ID, "id_great-account-choice_2", type=ElementType.RADIO, is_visible=False
        ),
        "i do not know where to enter my verification code": Selector(
            By.ID, "id_great-account-choice_3", type=ElementType.RADIO, is_visible=False
        ),
        "i have not received my letter containing the verification code": Selector(
            By.ID, "id_great-account-choice_4", type=ElementType.RADIO, is_visible=False
        ),
        "other": Selector(
            By.ID, "id_great-account-choice_5", type=ElementType.RADIO, is_visible=False
        ),
        "submit": SUBMIT_BUTTON,
        "back": Selector(
            By.CSS_SELECTOR,
            "form button[name='wizard_goto_step']",
            type=ElementType.LINK,
        ),
    }
}

POs = {
    "i have not received an email confirmation": contact_us_triage_great_account_dedicated_support_content,
    "i need to reset my password": contact_us_triage_great_account_dedicated_support_content,
    "my companies house login is not working": contact_us_triage_great_account_dedicated_support_content,
    "i do not know where to enter my verification code": contact_us_triage_great_account_dedicated_support_content,
    "i have not received my letter containing the verification code": contact_us_triage_great_account_dedicated_support_content,
    "other": contact_us_short_domestic,
}


def visit(driver: WebDriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL)


def should_see_form_choices(driver: WebDriver, names: List[str]):
    radio_selectors = get_selectors(SELECTORS["form"], ElementType.RADIO)
    for name in names:
        radio_selector = radio_selectors[name.lower()]
        find_element(driver, radio_selector, element_name=name, wait_for_it=False)
    logging.debug(
        f"All expected form choices: '{names}' are visible on " f"{driver.current_url}"
    )


def pick_radio_option_and_submit(driver: WebDriver, name: str) -> ModuleType:
    radio_selectors = get_selectors(SELECTORS["form"], ElementType.RADIO)
    choose_one_form_option(driver, radio_selectors, name)
    take_screenshot(driver, "Before submitting the form")
    button = find_element(
        driver, SUBMIT_BUTTON, element_name="Submit button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, "After submitting the form")
    return POs[name.lower()]


def pick_random_radio_option_and_submit(driver: WebDriver, ignored: List[str]):
    radio_selectors = get_selectors(SELECTORS["form"], ElementType.RADIO)
    selected = choose_one_form_option_except(driver, radio_selectors, ignored)
    take_screenshot(driver, "Before submitting the form")
    button = find_element(
        driver, SUBMIT_BUTTON, element_name="Submit button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, "After submitting the form")
    return POs[selected.lower()]


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)