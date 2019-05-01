# -*- coding: utf-8 -*-
"""Selling Online Overseas - Search results page"""
import logging
import random
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Selector,
    assertion_msg,
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
from settings import SELLING_ONLINE_OVERSEAS_UI_URL

SERVICE = "Selling Online Overseas"
TYPE = "search"
NAME = "Search results"
URL = urljoin(SELLING_ONLINE_OVERSEAS_UI_URL, "markets/results/")
PAGE_TITLE = "Search results | Selling online overseas"

SEARCH_BUTTON = Selector(
    By.CSS_SELECTOR, "#results-form input", type=ElementType.BUTTON
)
SELECTORS = {
    "search form": {
        "category": Selector(
            By.CSS_SELECTOR, "select[name=category_id]", type=ElementType.SELECT
        ),
        "country": Selector(
            By.CSS_SELECTOR, "select[name=country_id]", type=ElementType.SELECT
        ),
        "find a marketplace": SEARCH_BUTTON,
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


def open_random_marketplace(driver: WebDriver):
    selector = Selector(By.CSS_SELECTOR, "div.market-item-inner a")
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
    logging.debug(f"Collated list of products & countries: {list_of_values}")
    return list_of_values


def generate_form_details(country: str = None, category: str = None) -> dict:
    if category:
        category = category.replace("&", "&amp;")
        category = search_criteria.CATEGORIES[category]
    if country:
        country = country.replace("&", "&amp;")
        country = search_criteria.COUNTRIES[country]
    result = {"category": category, "country": country}
    logging.debug(f"Form details: {result}")
    return result


def search(driver: WebDriver, country: str, category: str):
    form_selectors = SELECTORS["search form"]
    find_a_marketplace = find_element(
        driver, SEARCH_BUTTON, element_name="find a marketplace"
    )
    scroll_to(driver, find_a_marketplace)
    details = generate_form_details(country, category)
    pick_option(driver, form_selectors, form_details=details)
    find_a_marketplace.click()
    take_screenshot(driver, "After submitting the form")


def should_see_marketplaces(driver: WebDriver, country: str):
    expected_countries = [country, "Global"]
    markets_selector = Selector(By.CSS_SELECTOR, "div.market-item-inner")
    marketplace_countries = {
        marketplace.find_element_by_tag_name("a")
        .text: marketplace.find_element_by_css_selector(
            "div.market-item-inner p.market-operating-countries"
        )
        .text
        for marketplace in find_elements(driver, markets_selector)
    }

    error = f"Found marketplace without a list of countries it operates in"
    assert marketplace_countries, error

    for marketplace, countries in marketplace_countries.items():
        with assertion_msg(
            f"{marketplace} does not operate in '{country}' or Globally!"
            f"but in '{countries}' instead"
        ):
            assert any(country in countries for country in expected_countries)
            logging.debug(
                f"{marketplace} operates in '{country}' or Globally! -> {countries}"
            )
