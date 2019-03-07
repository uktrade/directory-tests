# -*- coding: utf-8 -*-
"""Selling Online Overseas Home Page Object."""
import logging
import random
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Selector,
    check_url,
    find_and_click_on_page_element,
    find_elements,
    go_to_url,
    take_screenshot,
)
from settings import SELLING_ONLINE_OVERSEAS_UI_URL

SERVICE = "Selling Online Overseas"
TYPE = "search"
NAME = "Search results"
URL = urljoin(SELLING_ONLINE_OVERSEAS_UI_URL, "markets/results/")
PAGE_TITLE = "Search results | Selling online overseas"

SUBMIT_BUTTON = Selector(
    By.CSS_SELECTOR, "form button[type=submit]", type=ElementType.BUTTON
)
SELECTORS = {
    "expected elements": {
        "hero section": Selector(By.CSS_SELECTOR, ".hero-content"),
        "what do you sell input": Selector(By.ID, "search-product"),
        "where do you want to sell input": Selector(By.ID, "search-country"),
        "start his search now": Selector(By.CSS_SELECTOR, "form button"),
    }
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)


def open_any_marketplace(driver: WebDriver):
    selector = Selector(By.CSS_SELECTOR, ".markets-info > a")
    links = find_elements(driver, selector)
    random.choice(links).click()
