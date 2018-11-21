# -*- coding: utf-8 -*-
"""Export Readiness - Contact us - Triage location"""
import logging
from typing import List
from types import ModuleType

from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Selector,
    check_url,
    find_element,
    go_to_url,
    take_screenshot,
    choose_one_form_option,
    get_selectors,
)
from pages.exread import (
    contact_us_triage_domestic,
    contact_us_triage_international,
)
from settings import EXRED_UI_URL

NAME = "Contact Us"
SERVICE = "Export Readiness"
TYPE = "Contact us"
URL = urljoin(EXRED_UI_URL, "contact/triage/location/")
PAGE_TITLE = "Welcome to great.gov.uk"

THE_UK = Selector(By.ID, "id_location-choice_0", type=ElementType.RADIO, is_visible=False)
OUTSIDE_THE_UK = Selector(By.ID, "id_location-choice_1", type=ElementType.RADIO, is_visible=False)
SUBMIT_BUTTON = Selector(By.CSS_SELECTOR, "form button[type=submit]", type=ElementType.BUTTON)
SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#lede form"),
        "the uk": Selector(By.ID, "id_location-choice_0", type=ElementType.RADIO, is_visible=False),
        "outside the uk": Selector(By.ID, "id_location-choice_1", type=ElementType.RADIO, is_visible=False),
        "submit": SUBMIT_BUTTON,
    }
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
        find_element(
            driver, radio_selector, element_name=name, wait_for_it=False
        )
    logging.debug(
        f"All expected form choices: '{names}' are visible on "
        f"{driver.current_url}")


def pick_radio_option_and_submit(driver: WebDriver, name: str) -> ModuleType:
    radio_selectors = get_selectors(SELECTORS["form"], ElementType.RADIO)
    choose_one_form_option(driver, radio_selectors, name)
    take_screenshot(driver, "Before submitting the form")
    button = find_element(
        driver, SUBMIT_BUTTON, element_name="Submit button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, "After submitting the form")
    if name.lower() == "the uk":
        return contact_us_triage_domestic
    else:
        return contact_us_triage_international
