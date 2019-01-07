# -*- coding: utf-8 -*-
"""Export Readiness - Office finder search results page"""
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Selector,
    check_url,
    fill_out_input_fields,
    find_element,
    go_to_url,
    take_screenshot,
)
from settings import EXRED_UI_URL

NAME = "New Office Finder"
SERVICE = "Export Readiness"
TYPE = "office finder"
URL = urljoin(EXRED_UI_URL, "contact/office-finder/")
PAGE_TITLE = "Welcome to great.gov.uk"

SEARCH_BUTTON = Selector(
    By.CSS_SELECTOR, "form button[type=submit]", type=ElementType.BUTTON
)
SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "form[method=get]"),
        "postcode": Selector(By.ID, "id_postcode", type=ElementType.INPUT),
        "search": SEARCH_BUTTON,
    }
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)


def find_trade_office(driver: WebDriver, post_code: str):
    form_selectors = SELECTORS["form"]
    details = {"postcode": post_code}
    fill_out_input_fields(driver, form_selectors, details)
    take_screenshot(driver, "After filling out the form")
    button = find_element(
        driver, SEARCH_BUTTON, element_name="Search button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, "After submitting the form")
