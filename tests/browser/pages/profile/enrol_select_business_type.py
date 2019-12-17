# -*- coding: utf-8 -*-
"""Profile - Enrol - Select your business type"""
import logging
from types import ModuleType
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType, common_selectors
from pages.common_actions import (
    Selector,
    check_for_sections,
    check_url,
    choose_one_form_option,
    find_element,
    get_selectors,
    go_to_url,
    submit_form,
)
from pages.profile import (
    enrol_enter_your_business_email_and_set_password,
    enrol_sole_trader_enter_your_email_and_set_password,
    enrol_uk_taxpayer_enter_your_email_and_set_password,
    enrol_you_cannot_create_account,
)

NAME = "Select your business type"
SERVICE = Service.PROFILE
TYPE = PageType.FORM
URL = URLs.PROFILE_ENROL_SELECT_BUSINESS_TYPE.absolute
PAGE_TITLE = ""

SELECTORS = {
    "enrolment progress bar": {"itself": Selector(By.ID, "progress-column")},
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "section form"),
        "ltd, plc or royal charter": Selector(
            By.CSS_SELECTOR,
            "input[value='companies-house-company'] ~ label",
            type=ElementType.RADIO,
            is_visible=False,
        ),
        "sole trader or other type of business": Selector(
            By.CSS_SELECTOR,
            "input[value='non-companies-house-company'] ~ label",
            type=ElementType.RADIO,
            is_visible=False,
        ),
        "uk taxpayer": Selector(
            By.CSS_SELECTOR,
            "input[value='not-company'] ~ label",
            type=ElementType.RADIO,
            is_visible=False,
        ),
        "overseas company": Selector(
            By.CSS_SELECTOR,
            "input[value='overseas-company'] ~ label",
            type=ElementType.RADIO,
            is_visible=False,
        ),
        "submit": Selector(
            By.CSS_SELECTOR, "form button.button", type=ElementType.SUBMIT
        ),
    },
}
SELECTORS.update(common_selectors.DOMESTIC_HEADER)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.DOMESTIC_FOOTER)

POs = {
    "ltd, plc or royal charter": enrol_enter_your_business_email_and_set_password,
    "sole trader or other type of business": enrol_sole_trader_enter_your_email_and_set_password,
    "uk taxpayer": enrol_uk_taxpayer_enter_your_email_and_set_password,
    "overseas company": enrol_you_cannot_create_account,
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


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
    submit_form(driver, SELECTORS["form"])
    return POs[name.lower()]
