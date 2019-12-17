# -*- coding: utf-8 -*-
"""ERP - Consumer type"""
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
    check_form_choices,
    check_url,
    go_to_url,
    pick_one_option_and_submit,
)
from pages.erp import consumer_group_details, consumer_personal_details

NAME = "Consumer type (UK consumer)"
SERVICE = Service.ERP
TYPE = PageType.FORM
URL = URLs.ERP_CONSUMER_TYPE.absolute
PAGE_TITLE = ""

SELECTORS = {
    "form": {
        "form itself": Selector(By.CSS_SELECTOR, "#content form[method='post']"),
        "consumer group": Selector(
            By.CSS_SELECTOR,
            "input[value='CONSUMER_GROUP']",
            type=ElementType.RADIO,
            is_visible=False,
            next_page=consumer_group_details,
        ),
        "individual consumer": Selector(
            By.CSS_SELECTOR,
            "input[value='INDIVIDUAL_CONSUMER']",
            type=ElementType.RADIO,
            is_visible=False,
            next_page=consumer_personal_details,
        ),
        "continue": Selector(
            By.CSS_SELECTOR,
            "#content > form button.govuk-button",
            type=ElementType.SUBMIT,
        ),
    }
}
SELECTORS.update(common_selectors.ERP_HEADER)
SELECTORS.update(common_selectors.ERP_BETA)
SELECTORS.update(common_selectors.ERP_BACK)
SELECTORS.update(common_selectors.ERP_SAVE_FOR_LATER)
SELECTORS.update(common_selectors.ERP_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=False)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def should_see_form_choices(driver: WebDriver, names: List[str]):
    check_form_choices(driver, SELECTORS["form"], names)


def pick_radio_option_and_submit(driver: WebDriver, name: str) -> ModuleType:
    return pick_one_option_and_submit(
        driver, SELECTORS["form"], name, submit_button_name="continue"
    )
