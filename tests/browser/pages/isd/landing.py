# -*- coding: utf-8 -*-
"""Find a Supplier - ISD Landing page"""
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import common_selectors
from pages.common_actions import (
    Selector,
    check_for_sections,
    check_url,
    find_and_click_on_page_element,
    find_element,
    find_selector_by_name,
    go_to_url,
    take_screenshot,
)

NAME = "Landing"
SERVICE = Service.ISD
TYPE = PageType.LANDING
URL = URLs.ISD_LANDING.absolute
PAGE_TITLE = ""


SELECTORS = {
    "search form": {
        "itself": Selector(By.CSS_SELECTOR, "#hero form"),
        "search box": Selector(By.ID, "id_q"),
        "search button": Selector(By.CSS_SELECTOR, "#hero form button"),
    },
    "benefits": {
        "itself": Selector(By.ID, "benefits"),
        "heading": Selector(By.CSS_SELECTOR, "#benefits h2"),
        "list of benefits": Selector(By.CSS_SELECTOR, "#benefits ul li"),
    },
    "search categories": {
        "itself": Selector(By.ID, "bottom"),
        "heading": Selector(By.CSS_SELECTOR, "#bottom h2"),
        "categories": Selector(By.CSS_SELECTOR, "#bottom h3"),
        "category links": Selector(By.CSS_SELECTOR, "#bottom ul li a"),
    },
}
SELECTORS.update(common_selectors.INTERNATIONAL_HEADER_WO_LANGUAGE_SELECTOR)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.INTERNATIONAL_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=False)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def search(driver: WebDriver, *, keyword: str = None, sector: str = None):
    search_box_selector = find_selector_by_name(SELECTORS, "search box")
    input_field = find_element(
        driver, search_box_selector, element_name="Search box", wait_for_it=False
    )
    input_field.clear()
    input_field.send_keys(keyword)
    take_screenshot(driver, NAME + " after entering the keyword")
    find_and_click_on_page_element(
        driver, SELECTORS, element_name="search button", wait_for_it=False
    )
    take_screenshot(driver, NAME + " after submitting the search form")
