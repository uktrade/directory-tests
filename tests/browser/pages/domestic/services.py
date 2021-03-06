# -*- coding: utf-8 -*-
"""Domestic - Services page"""
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType, common_selectors
from pages.common_actions import Selector, check_for_sections, check_url, go_to_url
from pages.domestic import actions as domestic_actions

NAME = "Services"
SERVICE = Service.DOMESTIC
TYPE = PageType.LISTING
URL = URLs.DOMESTIC_SERVICES.absolute

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
SELECTORS.update(common_selectors.DOMESTIC_HEADER)
SELECTORS.update(common_selectors.SSO_LOGGED_OUT)
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
