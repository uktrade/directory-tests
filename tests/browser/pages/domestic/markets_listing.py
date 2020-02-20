# -*- coding: utf-8 -*-
"""Domestic Markets Page object"""

import logging
import random
from types import ModuleType
from typing import List, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from directory_tests_shared.utils import check_url_path_matches_template
from pages import ElementType, common_selectors
from pages.common_actions import (
    Actor,
    Selector,
    check_for_sections,
    check_url,
    go_to_url,
    pick_option,
    submit_form,
    wait_for_page_load_after_action,
)
from pages.domestic import actions, markets_listing as SELF

NAME = "Markets listing"
SERVICE = Service.DOMESTIC
TYPE = PageType.LISTING
URL = URLs.DOMESTIC_MARKETS.absolute

NAMES = [NAME, "filtered markets listing"]
SubURLs = {
    NAME: URL,
    "filtered markets listing": URLs.DOMESTIC_MARKETS_FILTERED.absolute_template,
}
SubURLs = {key.lower(): val for key, val in SubURLs.items()}

SELECTORS = {
    "form": {
        "sector selector": Selector(By.ID, "id_sector", type=ElementType.SELECT),
        "submit": Selector(
            By.CSS_SELECTOR,
            "#id_sector-container ~ button",
            type=ElementType.SUBMIT,
            next_page=SELF,
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


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def search(driver: WebDriver, phrase: str):
    actions.search(driver, phrase)


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


def open_random_marketplace(driver: WebDriver) -> str:
    card_links = driver.find_elements_by_css_selector("a.card-link")
    link = random.choice(card_links)
    link_text = link.text
    logging.debug(f"Randomly selected market is: {link_text}")
    with wait_for_page_load_after_action(driver):
        link.click()
    return link_text
