# -*- coding: utf-8 -*-
"""Domestic - Join our export community - landing page"""
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import Service
from pages import ElementType, common_selectors
from pages.common_actions import (
    Selector,
    check_for_sections,
    check_url,
    go_to_url,
    take_screenshot,
)
from pages.domestic import actions as domestic_actions

NAME = "Join our export community"
SERVICE = Service.DOMESTIC
TYPE = "landing"
URL = URLs.DOMESTIC_COMMUNITY.absolute

SELECTORS = {
    "share on social media": {"itself": Selector(By.CSS_SELECTOR, "ul.sharing-links")},
    "description": {
        "header": Selector(By.CSS_SELECTOR, "article header"),
        "heading": Selector(By.CSS_SELECTOR, "h1.heading-xlarge"),
        "sign up": Selector(
            By.CSS_SELECTOR, "p.body-text a.link", type=ElementType.LINK
        ),
    },
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
