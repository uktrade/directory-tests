# -*- coding: utf-8 -*-
"""ERP - Product Search - UK consumer"""
import logging
from random import choice
from types import ModuleType
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType, common_selectors
from pages.common_actions import (
    Selector,
    check_for_sections,
    check_url,
    find_elements,
    go_to_url,
    is_element_present,
    take_screenshot,
    wait_for_page_load_after_action,
)
from pages.erp import consumer_product_detail

NAME = "Product search (UK consumer)"
SERVICE = Service.ERP
TYPE = PageType.FORM
URL = URLs.ERP_CONSUMER_PRODUCT_SEARCH.absolute
PAGE_TITLE = ""

SUBMIT_BUTTON = Selector(
    By.CSS_SELECTOR, "#content > form button.govuk-button", type=ElementType.BUTTON
)
SELECTORS = {
    "form": {
        "form itself": Selector(By.CSS_SELECTOR, "#content form[method='post']"),
        "step counter": Selector(
            By.CSS_SELECTOR, "form[method=post] span.govuk-caption-l"
        ),
        "heading": Selector(By.CSS_SELECTOR, "form[method=post] h1"),
        "find a commodity code information page": Selector(
            By.CSS_SELECTOR, "form[method=post] div.govuk-inset-text a"
        ),
        "search": Selector(By.ID, "id_product-search-term", type=ElementType.INPUT),
        "search button": Selector(
            By.CSS_SELECTOR,
            "#id_product-search-term ~ button[form=search-form]",
            type=ElementType.BUTTON,
        ),
        "submit": SUBMIT_BUTTON,
    },
    "hierarchy codes": {
        "hierarchy codes heading": Selector(By.ID, "hierarchy-browser"),
        "first level": Selector(
            By.CSS_SELECTOR, "ul.app-hierarchy-tree li.app-hierarchy-tree__section"
        ),
    },
    "search results": {
        "expand to select": Selector(
            By.CSS_SELECTOR, "h2#search-results-title ~ section a"
        ),
        "select product code": Selector(
            By.CSS_SELECTOR, "h2#search-results-title ~ section button"
        ),
    },
}
SELECTORS.update(common_selectors.ERP_HEADER)
SELECTORS.update(common_selectors.ERP_BETA)
SELECTORS.update(common_selectors.ERP_BACK)
SELECTORS.update(common_selectors.ERP_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def drill_down_hierarchy_tree(driver: WebDriver) -> ModuleType:
    first_level_selector = Selector(
        By.CSS_SELECTOR, "ul.app-hierarchy-tree li.app-hierarchy-tree__section"
    )
    first_level = find_elements(driver, first_level_selector)
    first = choice(first_level)
    first_id = first.get_property("id")

    with wait_for_page_load_after_action(driver):
        logging.debug(f"First level: {first_id} -> {first.text}")
        first.click()

    select_code_selector = Selector(By.CSS_SELECTOR, "div.app-hierarchy-button")
    select_product_codes_present = is_element_present(driver, select_code_selector)
    logging.debug(
        f"Is Select product code button present: {select_product_codes_present}"
    )

    current_parent_id = first_id
    while not select_product_codes_present:
        child_level_selector = Selector(
            By.CSS_SELECTOR, f"#{current_parent_id} ul li.app-hierarchy-tree__chapter"
        )
        child_level = find_elements(driver, child_level_selector)
        if not child_level:
            logging.debug("No more child level elements")
            break
        logging.debug(f"Child elements of '{current_parent_id}' are: {child_level}")
        child = choice(child_level)
        current_parent_id = child.get_property("id")

        with wait_for_page_load_after_action(driver, timeout=5):
            logging.debug(f"Selected child: {current_parent_id}")
            child.click()

        logging.debug(
            f"Is Select product code button present: {select_product_codes_present}"
        )
        select_product_codes_present = is_element_present(driver, select_code_selector)

    if select_product_codes_present:
        select_codes = find_elements(driver, select_code_selector)
        select = choice(select_codes)
        select_id = select.get_property("id")
        logging.debug(f"Selected product code: {select_id}")
        with wait_for_page_load_after_action(driver, timeout=5):
            select.click()
    else:
        logging.error("Strange! Could not find 'Select' product codes button")

    return consumer_product_detail
