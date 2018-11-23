# -*- coding: utf-8 -*-
"""Export Readiness - Domestic Contact us - What can we help you with?"""
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
    choose_one_form_option,
    find_and_click_on_page_element,
    find_element,
    get_selectors,
    go_to_url,
    take_screenshot,
)
from pages.exread import (
    contact_us_long_export_advice_comment,
    contact_us_triage_great_services,
    ukef_what_would_you_like_to_know,
)
from pages.external import office_finder
from settings import EXRED_UI_URL

NAME = "What can we help you with?"
SERVICE = "Export Readiness"
TYPE = "Domestic Contact us"
URL = urljoin(EXRED_UI_URL, "contact/triage/domestic/")
PAGE_TITLE = "Welcome to great.gov.uk"

SUBMIT_BUTTON = Selector(By.CSS_SELECTOR, "form button[type=submit]", type=ElementType.BUTTON)
SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#lede form"),
        "find your local trade office": Selector(By.ID, "id_domestic-choice_0", type=ElementType.RADIO, is_visible=False),
        "advice to export from the uk": Selector(By.ID, "id_domestic-choice_1", type=ElementType.RADIO, is_visible=False),
        "great.gov.uk account and services support": Selector(By.ID, "id_domestic-choice_2", type=ElementType.RADIO, is_visible=False),
        "uk export finance (ukef)": Selector(By.ID, "id_domestic-choice_3", type=ElementType.RADIO, is_visible=False),
        "eu exit": Selector(By.ID, "id_domestic-choice_4", type=ElementType.RADIO, is_visible=False),
        "events": Selector(By.ID, "id_domestic-choice_5", type=ElementType.RADIO, is_visible=False),
        "defence and security organisation (dso)": Selector(By.ID, "id_domestic-choice_6", type=ElementType.RADIO, is_visible=False),
        "other": Selector(By.ID, "id_domestic-choice_7", type=ElementType.RADIO, is_visible=False),
        "submit": SUBMIT_BUTTON,
        "back": Selector(By.CSS_SELECTOR, "form button[name='wizard_goto_step']", type=ElementType.LINK)
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
    POs = {
        "find your local trade office": office_finder,
        "advice to export from the uk": contact_us_long_export_advice_comment,
        "great.gov.uk account and services support": contact_us_triage_great_services,
        "uk export finance (ukef)": ukef_what_would_you_like_to_know,
        "eu exit": None,
        "events": None,
        "defence and security organisation (dso)": None,
        "other": None,
    }
    return POs[name.lower()]


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)
