# -*- coding: utf-8 -*-
"""Profile - Enrol - You cannot create an account page"""
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import common_selectors
from pages.common_actions import (
    Selector,
    check_for_sections,
    check_url,
    go_to_url,
    take_screenshot,
)

NAME = "You cannot create an account"
SERVICE = Service.PROFILE
TYPE = PageType.FORM
URL = URLs.PROFILE_ENROL_OVERSEAS_BUSINESS.absolute
PAGE_TITLE = ""

SELECTORS = {
    "explanation": {
        "heading": Selector(By.CSS_SELECTOR, "#content div > h1"),
        "back": Selector(By.PARTIAL_LINK_TEXT, "Back"),
        "visit our site for international businesses": Selector(
            By.PARTIAL_LINK_TEXT, "visit our site for international businesses."
        ),
    }
}
SELECTORS.update(common_selectors.DOMESTIC_HEADER)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.DOMESTIC_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL)
    msg = f"Got 404 on {driver.current_url}"
    assert "This page cannot be found" not in driver.page_source, msg


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)
