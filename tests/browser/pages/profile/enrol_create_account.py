# -*- coding: utf-8 -*-
"""Profile - Enrol - Create an account"""
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Selector,
    check_url,
    find_and_click_on_page_element,
    go_to_url,
    take_screenshot,
)
from settings import DIRECTORY_UI_PROFILE_URL

NAME = "Create an account"
SERVICE = "Profile"
TYPE = "Enrol"
URL = urljoin(DIRECTORY_UI_PROFILE_URL, "enrol/")
PAGE_TITLE = ""

SELECTORS = {
    "enrolment progress bar": {
        "itself": Selector(By.ID, "start-page-progress-indicator"),
        "start now": Selector(
            By.ID, "start-now-button", type=ElementType.LINK
        ),
    }
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL)


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)
