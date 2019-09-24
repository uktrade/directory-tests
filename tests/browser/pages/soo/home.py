# -*- coding: utf-8 -*-
"""Selling Online Overseas Home Page Object."""
import logging
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType, common_selectors
from pages.common_actions import (
    Selector,
    check_url,
    find_and_click_on_page_element,
    find_element,
    find_elements,
    go_to_url,
    pick_option,
    scroll_to,
    take_screenshot,
)
from pages.soo import search_criteria
from directory_tests_shared.enums import Service
from directory_tests_shared.settings import SOO_URL

NAME = "Home"
URL = SOO_URL
SERVICE = Service.SOO
TYPE = "home"
PAGE_TITLE = "Welcome to Selling online overseas"

SEARCH_BUTTON = Selector(
    By.CSS_SELECTOR, "#results-form button[type='submit']", type=ElementType.BUTTON
)

SELECTORS = {
    "hero": {"itself": Selector(By.CSS_SELECTOR, ".hero-content")},
    "search form": {
        "category": Selector(
            By.CSS_SELECTOR, "select[name=category_id]", type=ElementType.SELECT
        ),
        "country": Selector(
            By.CSS_SELECTOR, "select[name=country_id]", type=ElementType.SELECT
        ),
        "find your marketplace": SEARCH_BUTTON,
    },
}
SELECTORS.update(common_selectors.HEADER)
SELECTORS.update(common_selectors.FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)


def open_random_marketplace(driver: WebDriver):
    selector = Selector(By.CSS_SELECTOR, "#random-markets a.card-link")
    links = find_elements(driver, selector)
    random.choice(links).click()


def generate_form_details(country: str = None, category: str = None) -> dict:
    if category:
        category = search_criteria.CATEGORIES[category]
    if country:
        country = search_criteria.COUNTRIES[country]
    result = {"category": category, "country": country}
    logging.debug(f"Form details: {result}")
    return result


def search(driver: WebDriver, country: str, category: str):
    form_selectors = SELECTORS["search form"]
    find_a_marketplace = find_element(
        driver, SEARCH_BUTTON, element_name="find your marketplace"
    )
    scroll_to(driver, find_a_marketplace)
    details = generate_form_details(country, category)
    pick_option(driver, form_selectors, form_details=details)
    find_a_marketplace.click()
    take_screenshot(driver, "After submitting the form")
