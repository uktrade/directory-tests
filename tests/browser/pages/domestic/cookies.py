# -*- coding: utf-8 -*-
"""Domestic - Cookies - form page"""
import logging
from types import ModuleType
from typing import List, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType, common_selectors
from pages.common_actions import (
    Actor,
    Selector,
    check_for_sections,
    check_radio,
    check_url,
    go_to_url,
    submit_form,
)
from pages.domestic import actions as domestic_actions, cookies

NAME = "Cookies"
SERVICE = Service.DOMESTIC
TYPE = PageType.FORM
URL = URLs.DOMESTIC_COOKIES.absolute

SELECTORS = {
    "form": {
        "itself": Selector(By.ID, "cookie-preferences-form"),
        "find more about cookies": Selector(
            By.CSS_SELECTOR, "#cookie-preferences-form a"
        ),
        "allow measure website use": Selector(
            By.ID, "cookies-usage-on", type=ElementType.RADIO
        ),
        "do not measure website use": Selector(
            By.ID, "cookies-usage-off", type=ElementType.RADIO
        ),
        "allow use for marketing campaigns": Selector(
            By.ID, "cookies-campaigns-on", type=ElementType.RADIO
        ),
        "do not use for marketing campaigns": Selector(
            By.ID, "cookies-campaigns-off", type=ElementType.RADIO
        ),
        "allow to remember my settings": Selector(
            By.ID, "cookies-settings-on", type=ElementType.RADIO
        ),
        "do not remember my settings": Selector(
            By.ID, "cookies-settings-off", type=ElementType.RADIO
        ),
        "save changes": Selector(
            By.CSS_SELECTOR,
            "#cookie-preferences-form button",
            type=ElementType.SUBMIT,
            next_page=cookies,
        ),
    },
    "confirmation banner": {
        "itself": Selector(By.CSS_SELECTOR, "#content div.confirmation-banner"),
        "heading": Selector(By.CSS_SELECTOR, "#content div.confirmation-banner h3"),
        "message": Selector(By.CSS_SELECTOR, "#content div.confirmation-banner p"),
    },
}
SELECTORS.update(common_selectors.DOMESTIC_HEADER)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.DOMESTIC_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def search(driver: WebDriver, phrase: str):
    domestic_actions.search(driver, phrase)


def generate_form_details(actor: Actor, *, custom_details: dict = None) -> dict:
    result = {
        "allow measure website use": False,
        "allow use for marketing campaigns": False,
        "allow to remember my settings": False,
        "do not measure website use": True,
        "do not use for marketing campaigns": True,
        "do not remember my settings": True,
    }
    if custom_details:
        result.update(custom_details)

    logging.debug(f"Generated form details: {result}")
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    check_radio(driver, form_selectors, details)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"], wait_for_new_page_to_load=False)
