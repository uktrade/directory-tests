# -*- coding: utf-8 -*-
"""ERP - Product Search - UK consumer"""
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
    check_form_choices,
    check_url,
    go_to_url,
    pick_one_option_and_submit,
    take_screenshot,
)

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
SELECTORS.update(common_selectors.ERP_BREADCRUMBS)
SELECTORS.update(common_selectors.ERP_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def should_see_form_choices(driver: WebDriver, names: List[str]):
    check_form_choices(driver, SELECTORS["form"], names)


def pick_radio_option_and_submit(driver: WebDriver, name: str) -> ModuleType:
    return pick_one_option_and_submit(driver, SELECTORS["form"], name)
