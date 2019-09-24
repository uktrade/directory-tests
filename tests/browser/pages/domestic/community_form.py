# -*- coding: utf-8 -*-
"""Domestic - Join our export community - form page"""
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType, common_selectors
from pages.common_actions import (
    Selector,
    check_for_sections,
    check_url,
    go_to_url,
    take_screenshot,
)
from pages.domestic import actions as domestic_actions
from directory_tests_shared.enums import Service
from directory_tests_shared.settings import DOMESTIC_URL

NAME = "Join our export community"
SERVICE = Service.DOMESTIC
TYPE = "form"
URL = urljoin(DOMESTIC_URL, "community/join/")

SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "form[method=POST]"),
        "name": Selector(By.ID, "id_name", type=ElementType.INPUT),
        "email": Selector(By.ID, "id_email", type=ElementType.INPUT),
        "phone number": Selector(By.ID, "id_phone_number", type=ElementType.INPUT),
        "company name": Selector(By.ID, "id_company_name", type=ElementType.INPUT),
        "location": Selector(By.ID, "id_company_location", type=ElementType.INPUT),
        "sector": Selector(By.ID, "id_sector", type=ElementType.INPUT),
        "website": Selector(By.ID, "id_company_website", type=ElementType.SELECT),
        "number of employees": Selector(
            By.ID, "id_employees_number", type=ElementType.SELECT
        ),
        "yes": Selector(By.ID, "id_currently_export_0", type=ElementType.RADIO),
        "no": Selector(By.ID, "id_currently_export_1", type=ElementType.RADIO),
        "where did you hear about": Selector(
            By.ID, "id_advertising_feedback", type=ElementType.SELECT
        ),
        "t&c": Selector(By.ID, "id_terms_agreed", type=ElementType.CHECKBOX),
        "submit": Selector(By.CSS_SELECTOR, "button.button", type=ElementType.BUTTON),
    }
}
SELECTORS.update(common_selectors.HEADER)
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


def search(driver: WebDriver, phrase: str):
    domestic_actions.search(driver, phrase)
