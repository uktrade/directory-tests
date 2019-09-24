# -*- coding: utf-8 -*-
"""PIR - Landing Page"""
import logging
from typing import List
from urllib.parse import urljoin

from directory_tests_shared.enums import Service
from directory_tests_shared.settings import DOMESTIC_URL
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

NAME = "Landing"
SERVICE = Service.PIR
TYPE = "landing"
URL = urljoin(DOMESTIC_URL, "international/invest/perfectfit/")

SUBMIT_BUTTON = Selector(
    By.CSS_SELECTOR, "form input.button[type=submit]", type=ElementType.BUTTON
)
SELECTORS = {
    "hero": {
        "self": Selector(By.ID, "hero"),
        "heading": Selector(By.CSS_SELECTOR, "#hero h1"),
    },
    "contact form": {
        "itself": Selector(By.CSS_SELECTOR, "#content form"),
        "name": Selector(By.ID, "id_name", type=ElementType.INPUT),
        "company": Selector(By.ID, "id_company", type=ElementType.INPUT),
        "email": Selector(By.ID, "id_email", type=ElementType.INPUT),
        "phone": Selector(By.ID, "id_phone_number", type=ElementType.INPUT),
        "country": Selector(By.ID, "id_country", type=ElementType.SELECT),
        "sector": Selector(By.ID, "id_sector", type=ElementType.SELECT),
        "send updates": Selector(
            By.ID, "id_gdpr_optin", type=ElementType.CHECKBOX, is_visible=False
        ),
        "submit": SUBMIT_BUTTON,
    },
}
SELECTORS.update(common_selectors.INTERNATIONAL_HEADER_WO_LANGUAGE_SELECTOR)
SELECTORS.update(common_selectors.INTERNATIONAL_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)
