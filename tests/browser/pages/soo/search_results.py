# -*- coding: utf-8 -*-
"""Selling Online Overseas Home Page Object."""
import logging
import random
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
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

SERVICE = "Selling Online Overseas"
TYPE = "search"
NAME = "Search results"
URL = urljoin(SELLING_ONLINE_OVERSEAS_UI_URL, "markets/results/")
PAGE_TITLE = "Search results | Selling online overseas"

SEARCH_BUTTON = Selector(
    By.CSS_SELECTOR, "form button[type=submit]", type=ElementType.BUTTON
)
SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "form[method=get]"),
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


def collate_products_and_countries(
    product_types: List[str], country_names: List[str]
) -> List[dict]:
    if len(product_types) > len(country_names):
        iterations = len(product_types)
    else:
        iterations = len(country_names)

    list_of_values = []
    for i in range(iterations):
        list_of_values.append(
            {
                "product_type": dict(enumerate(product_types)).get(i, None),
                "country_name": dict(enumerate(country_names)).get(i, None),
            }
        )
    return list_of_values


def search(
    driver: WebDriver, product_types: List[str], country_names: List[str]
):
    form_selectors = SELECTORS["form"]
    button = find_element(
        driver,
        SEARCH_BUTTON,
        element_name="start your search now",
        wait_for_it=True,
    )
    scroll_to(driver, button)
    values = collate_products_and_countries(product_types, country_names)

    for pair in values:
        fill_out_input_fields(driver, form_selectors, pair)
    button.click()
    take_screenshot(driver, "After submitting the form")


def should_see_marketplace(driver: WebDriver, country_names: str):
    countries = country_names.split(",")
    countries.append("Global")

    for country in countries:
        country_selector = Selector(
            By.XPATH, f"//dd[contains(text(), country)]"
        )
        find_element(
            driver, country_selector, element_name=country, wait_for_it=False
        )
        logging.debug(f"As expected {country} is present")
