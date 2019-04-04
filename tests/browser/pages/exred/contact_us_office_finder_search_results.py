# -*- coding: utf-8 -*-
"""Export Readiness - Sort Domestic Contact us form"""
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Selector,
    check_for_expected_sections_elements,
    check_url,
    fill_out_input_fields,
    find_element,
    find_selector_by_name,
    go_to_url,
    take_screenshot,
)
from settings import EXRED_UI_URL

NAME = "New Office Finder"
SERVICE = "Export Readiness"
TYPE = "search results"
URL = urljoin(EXRED_UI_URL, "contact/office-finder/")
PAGE_TITLE = "Welcome to great.gov.uk"

SEARCH_BUTTON = Selector(
    By.CSS_SELECTOR, "button.button", type=ElementType.BUTTON
)
SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "form[method=get]"),
        "postcode": Selector(By.ID, "id_postcode", type=ElementType.INPUT),
        "search": SEARCH_BUTTON,
    },
    "results": {
        "itself": Selector(By.ID, "results"),
        "office name": Selector(By.ID, "office-name"),
        "office address": Selector(By.CSS_SELECTOR, "#results > p:nth-child(4)"),
        "telephone": Selector(By.CSS_SELECTOR, "#results > p:nth-child(6)"),
        "contact button": Selector(By.CSS_SELECTOR, "#results > a"),
    },
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    check_for_expected_sections_elements(driver, SELECTORS)


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


def should_see_office_details(driver: WebDriver, trade_office: str, city: str):
    office_selector = find_selector_by_name(SELECTORS, "office name")
    office = find_element(driver, office_selector)
    error = f"Expected to find details for '{trade_office}' but got {office.text}"
    assert trade_office.lower() in office.text.lower(), error

    address_selector = find_selector_by_name(SELECTORS, "office address")
    address = find_element(driver, address_selector)
    error = (
        f"Expected to find details for trade office in '{city}' but got "
        f"{address.text}"
    )
    assert city.lower() in address.text.lower(), error
