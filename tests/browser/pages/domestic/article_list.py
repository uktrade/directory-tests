# -*- coding: utf-8 -*-
"""Domestic Article List Page Object."""
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared.enums import Service
from pages.common_actions import (
    Selector,
    check_for_expected_sections_elements,
    check_for_section,
    check_for_sections,
    check_if_element_is_not_visible,
    take_screenshot,
)

NAME = "Article List"
SERVICE = Service.DOMESTIC
TYPE = "article list"
URL = None

ARTICLE_CATEGORY = Selector(By.CSS_SELECTOR, "#content > section h1.title")
BREADCRUMBS = Selector(By.CSS_SELECTOR, "div.breadcrumbs")
LIST_OF_ARTICLES = Selector(By.ID, "js-paginate-list")
IS_THERE_ANYTHING_WRONG_WITH_THIS_PAGE_LINK = Selector(
    By.CSS_SELECTOR, "section.error-reporting a"
)

SELECTORS = {
    "hero": {
        "itself": Selector(By.CSS_SELECTOR, "#content > section.hero-section"),
        "heading title": ARTICLE_CATEGORY,
    },
    "breadcrumbs": {"breadcrumbs": BREADCRUMBS},
    "list of articles": {"itself": LIST_OF_ARTICLES},
    "error reporting": {
        "itself": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "report page link": IS_THERE_ANYTHING_WRONG_WITH_THIS_PAGE_LINK,
    },
}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    import copy

    all_except_save_progress = copy.copy(SELECTORS)
    all_except_save_progress.pop("save progress")
    check_for_expected_sections_elements(driver, all_except_save_progress)


def should_see_section(driver: WebDriver, name: str):
    check_for_section(driver, all_sections=SELECTORS, sought_section=name)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def should_not_see_section(driver: WebDriver, name: str):
    section = SELECTORS[name.lower()]
    for key, selector in section.items():
        check_if_element_is_not_visible(driver, selector, element_name=key)
