# -*- coding: utf-8 -*-
"""Get Finance Page Object."""
import logging
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    check_for_expected_sections_elements,
    check_if_element_is_not_visible,
    check_title,
    check_url,
    go_to_url,
    take_screenshot,
)
from settings import EXRED_UI_URL

NAME = "Get Finance"
SERVICE = "Export Readiness"
TYPE = "interim"
URL = urljoin(EXRED_UI_URL, "get-finance/")
PAGE_TITLE = "Get finance - great.gov.uk"

SELECTORS = {
    "breadcrumbs": {
        "itself": Selector(By.CSS_SELECTOR, "div.breadcrumbs"),
        "current page": Selector(
            By.CSS_SELECTOR, "div.breadcrumbs li[aria-current='page']"
        ),
    },
    "hero": {
        "itself": Selector(By.CSS_SELECTOR, "section.get-finance-banner"),
        "header": Selector(By.CSS_SELECTOR, "section.get-finance-banner h1"),
    },
    "video": {
        "itself": Selector(By.CSS_SELECTOR, "section.get-finance-video"),
        "header": Selector(By.CSS_SELECTOR, "section.get-finance-video h2"),
        "video": Selector(By.CSS_SELECTOR, "section.get-finance-video video"),
    },
    "error reporting": {
        "itself": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "link": Selector(By.ID, "error-reporting-section-contact-us"),
    },
}

UNEXPECTED_ELEMENTS = {
    "share widget": {
        "itself": Selector(By.CSS_SELECTOR, "ul.sharing-links"),
    },
    "article counters and indicators": {
        "itself": Selector(By.CSS_SELECTOR, "#top > div.scope-indicator"),
    },
    "tasks completed counter": {
        "itself": Selector(By.CSS_SELECTOR, ".TASKS_ARE_NOT_IMPLEMENTED_YES"),
    },
    "tasks total number": {
        "itself": Selector(By.CSS_SELECTOR, ".TASKS_ARE_NOT_IMPLEMENTED_YES"),
    },
    "total number of articles": {
        "itself": Selector(By.CSS_SELECTOR, "dd.position > span.to"),
    },
    "articles read counter": {
        "itself": Selector(By.CSS_SELECTOR, "dd.position > span.from"),
    },
    "time to complete remaining chapters": {
        "itself": Selector(By.CSS_SELECTOR, "dd.time span.value"),
    },
    "share menu": {
        "itself": Selector(By.CSS_SELECTOR, "ul.sharing-links"),
    }
}


def visit(driver: WebDriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    check_title(driver, PAGE_TITLE, exact_match=True)
    check_for_expected_sections_elements(driver, SELECTORS)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def check_elements_are_not_visible(driver: WebDriver, elements: list):
    take_screenshot(driver, NAME + " should not see some elements")
    for element_name in elements:
        selector = UNEXPECTED_ELEMENTS[element_name.lower()]
        check_if_element_is_not_visible(
            driver, selector, element_name=element_name, wait_for_it=False
        )


def should_not_see_section(driver: WebDriver, name: str):
    section = UNEXPECTED_ELEMENTS[name.lower()]
    for key, selector in section.items():
        check_if_element_is_not_visible(driver, selector, element_name=key)
