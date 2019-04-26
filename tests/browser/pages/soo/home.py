# -*- coding: utf-8 -*-
"""Selling Online Overseas Home Page Object."""
import random
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType, common_selectors
from pages.common_actions import (
    Selector,
    check_url,
    fill_out_input_fields,
    find_and_click_on_page_element,
    find_element,
    find_elements,
    go_to_url,
    scroll_to,
    take_screenshot,
)
from pages.soo.autocomplete_callbacks import (
    autocomplete_country_name,
    autocomplete_product_type,
)
from settings import SELLING_ONLINE_OVERSEAS_UI_URL

NAME = "Home"
URL = urljoin(SELLING_ONLINE_OVERSEAS_UI_URL, "")
SERVICE = "Selling Online Overseas"
TYPE = "home"
PAGE_TITLE = "Welcome to Selling online overseas"

SEARCH_BUTTON = Selector(
    By.CSS_SELECTOR, "#hero-banner form input.submit", type=ElementType.BUTTON
)

SELECTORS = {
    "expected elements": {
        "hero section": Selector(By.CSS_SELECTOR, ".hero-content"),
        "product_type": Selector(
            By.ID,
            "search-product",
            type=ElementType.INPUT,
            is_visible=False,
            autocomplete_callback=autocomplete_product_type,
        ),
        "country_name": Selector(
            By.ID,
            "search-country",
            type=ElementType.INPUT,
            is_visible=False,
            autocomplete_callback=autocomplete_country_name,
        ),
        "start your search now": SEARCH_BUTTON,
    }
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
    selector = Selector(By.CSS_SELECTOR, "ul.markets li.markets-item")
    links = find_elements(driver, selector)
    random.choice(links).click()


def collate_products_and_countries(
    products: List[str], countries: List[str]
) -> List[dict]:
    if len(products) > len(countries):
        iterations = len(products)
    else:
        iterations = len(countries)

    list_of_values = []
    for i in range(iterations):
        list_of_values.append(
            {
                "product_type": dict(enumerate(products)).get(i, None),
                "country_name": dict(enumerate(countries)).get(i, None),
            }
        )
    return list_of_values


def search(driver: WebDriver, products: List[str], countries: List[str]):
    form_selectors = SELECTORS["expected elements"]
    button = find_element(
        driver, SEARCH_BUTTON, element_name="start your search now", wait_for_it=True
    )
    scroll_to(driver, button)
    values = collate_products_and_countries(products, countries)

    for pair in values:
        fill_out_input_fields(driver, form_selectors, pair)
    button.click()
    take_screenshot(driver, "After submitting the form")
