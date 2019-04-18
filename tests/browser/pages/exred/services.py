# -*- coding: utf-8 -*-
"""ExRed - Services page"""
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType, common_selectors
from pages.common_actions import (
    Selector,
    check_for_sections,
    check_url,
    find_and_click_on_page_element,
    go_to_url,
    take_screenshot,
)
from pages.exred import actions as domestic_actions
from settings import EXRED_UI_URL

NAME = "Services"
SERVICE = "Export Readiness"
TYPE = "services list"
URL = urljoin(EXRED_UI_URL, "services/")

SELECTORS = {
    "services": {
        "service cards": Selector(By.CSS_SELECTOR, "div.card"),
        "create a business profile": Selector(
            By.ID, "find-a-buyer-link", type=ElementType.LINK
        ),
        "find online marketplaces": Selector(
            By.ID, "selling-online-overseas-link", type=ElementType.LINK
        ),
        "find export opportunities": Selector(
            By.ID, "export-opportunities-link", type=ElementType.LINK
        ),
        "uk export finance": Selector(
            By.ID, "uk-export-finance-link", type=ElementType.LINK
        ),
        "find events and visits": Selector(By.ID, "events-link", type=ElementType.LINK),
        "get an eori number": Selector(By.ID, "govuk-eori-link", type=ElementType.LINK),
    }
}
SELECTORS.update(common_selectors.HEADER)
SELECTORS.update(common_selectors.SSO_LOGGED_OUT)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)


def search(driver: WebDriver, phrase: str):
    domestic_actions.search(driver, phrase)
