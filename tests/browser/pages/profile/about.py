# -*- coding: utf-8 -*-
"""Profile - About"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import common_selectors
from pages.common_actions import (
    Selector,
    check_url,
    find_and_click_on_page_element,
    go_to_url,
    take_screenshot,
)

NAME = "About"
SERVICE = Service.PROFILE
TYPE = PageType.FORM
URL = URLs.PROFILE_ABOUT.absolute
PAGE_TITLE = ""

SELECTORS = {
    "tab bar": {
        "itself": Selector(By.CSS_SELECTOR, ".sso-profile-tab-container"),
        "export opportunities": Selector(By.LINK_TEXT, "Export opportunities"),
        "Business profile": Selector(By.LINK_TEXT, "Business profile"),
        "Selling online overseas": Selector(By.LINK_TEXT, "Selling online overseas"),
        "about": Selector(By.LINK_TEXT, "About"),
    },
    "welcome": {"welcome message": Selector(By.ID, "welcome-message")},
}
SELECTORS.update(common_selectors.DOMESTIC_HEADER)
SELECTORS.update(common_selectors.DOMESTIC_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL)


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)
