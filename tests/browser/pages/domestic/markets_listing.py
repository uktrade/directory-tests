# -*- coding: utf-8 -*-
"""Domestic Markets Page object"""

import logging
from types import ModuleType
from typing import Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from directory_tests_shared.utils import check_url_path_matches_template
from pages import ElementType, common_selectors
from pages.common_actions import (
    Actor,
    Selector,
    check_url,
    go_to_url,
    pick_option,
    submit_form,
)
from pages.domestic import actions as domestic_actions, markets_listing

NAME = "Markets listing"
SERVICE = Service.DOMESTIC
TYPE = PageType.LISTING
URL = URLs.DOMESTIC_MARKETS.absolute

NAMES = [NAME, "filtered markets listing"]
SubURLs = {
    NAME: URL,
    "filtered markets listing": URLs.DOMESTIC_MARKETS_FILTERED.absolute_template,
}

SELECTORS = {
    "form": {
        "sector selector": Selector(By.ID, "id_sector", type=ElementType.SELECT),
        "submit": Selector(
            By.CSS_SELECTOR,
            "#id_sector-container ~ button",
            type=ElementType.SUBMIT,
            next_page=markets_listing,
        ),
        "view all market guides": Selector(
            By.CSS_SELECTOR, "#id_sector-container ~ a", type=ElementType.LINK
        ),
    },
    "no results": {"itself": Selector(By.ID, "search-results-list")},
}
SELECTORS.update(common_selectors.DOMESTIC_HEADER)


def visit(driver: WebDriver, *, page_name: str = None):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver, *, page_name: str = None):
    if page_name:
        url = SubURLs[page_name]
        check_url_path_matches_template(url, driver.current_url)
    else:
        check_url(driver, URL, exact_match=False)


def search(driver: WebDriver, phrase: str):
    domestic_actions.search(driver, phrase)


def generate_form_details(actor: Actor, *, custom_details: dict = None) -> dict:
    result = {"sector selector": None}

    if custom_details:
        result.update(custom_details)

    logging.debug(f"Generated form details: {result}")
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    pick_option(driver, form_selectors, details)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
