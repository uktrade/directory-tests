# -*- coding: utf-8 -*-
"""Profile - Enrol - Start as Individual"""
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import common_selectors
from pages.common_actions import Selector, check_for_sections, check_url, go_to_url

NAME = "Start as Individual"
SERVICE = Service.PROFILE
TYPE = PageType.FORM
URL = URLs.PROFILE_ENROL_INDIVIDUAL_START.absolute
PAGE_TITLE = ""

SELECTORS = {
    "explanation": {
        "heading": Selector(By.CSS_SELECTOR, "#content > section h1"),
        "explanation": Selector(By.CSS_SELECTOR, "#content > section p"),
    },
    "links": {
        "links": Selector(By.CSS_SELECTOR, "#content > section ul a"),
        "continue creating account for individual": Selector(
            By.PARTIAL_LINK_TEXT, "Continue creating account for individual"
        ),
    },
}
SELECTORS.update(common_selectors.DOMESTIC_HEADER)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.DOMESTIC_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)
