# -*- coding: utf-8 -*-
"""Find a Supplier - Industries Page Object."""
import logging
from typing import List
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.common.by import By

from pages.common_actions import (
    AssertionExecutor,
    check_for_expected_sections_elements,
    check_for_section,
    check_for_sections,
    check_title,
    check_url,
    find_and_click_on_page_element,
    find_element,
    find_elements,
    go_to_url,
    take_screenshot,
    Selector
)
from settings import DIRECTORY_UI_SUPPLIER_URL

NAME = "Industries"
SERVICE = "Find a Supplier"
TYPE = "industries"
URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "industries/")
PAGE_TITLE = "Find the best UK suppliers for your industry - trade.great.gov.uk"

BREADCRUMB_LINKS = "p.breadcrumbs > a"
INDUSTRIES_BREADCRUMB = "p.breadcrumbs > span.current.bidi-rtl"
INDUSTRIES_LINKS = "#industry-pages-container > section a"
MORE_INDUSTRIES_LINKS = "#industry-pages-container > ul a"
SELECTORS = {
    "hero": {
        "itself": Selector(By.ID, "hero"),
        "header": Selector(By.CSS_SELECTOR, "#hero h1")},
    "breadcrumbs": {
        "itself": Selector(By.CSS_SELECTOR, "#content p.breadcrumbs"),
        "industries": Selector(By.CSS_SELECTOR, INDUSTRIES_BREADCRUMB),
    },
    "contact us": {
        "itself": Selector(By.ID, "introduction"),
        "header": Selector(By.CSS_SELECTOR, "#introduction p"),
        "contact us": Selector(By.CSS_SELECTOR, "#introduction a"),
    },
    "industries": {
        "itself": Selector(By.ID, "industry-pages-container"),
        "industries": Selector(By.CSS_SELECTOR, INDUSTRIES_LINKS),
    },
    "more industries": {
        "itself": Selector(By.CSS_SELECTOR, "#industry-pages-container > ul"),
        "more industries": Selector(By.CSS_SELECTOR, MORE_INDUSTRIES_LINKS,)
    },
}


def visit(driver: webdriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    check_title(driver, PAGE_TITLE, exact_match=True)
    check_for_expected_sections_elements(driver, SELECTORS)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(executor: AssertionExecutor, names: List[str]):
    check_for_sections(executor, all_sections=SELECTORS, sought_sections=names)


def click_on_page_element(driver: webdriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)


def clean_name(name: str) -> str:
    return name.replace("Find a Supplier - ", "").replace("industry", "").strip()


def open_industry(driver: webdriver, industry_name: str):
    industry_name = clean_name(industry_name)
    logging.debug("Looking for: {}".format(industry_name))
    industry_link = find_element(
        driver,
        by_link_text=industry_name,
        element_name="Industry card",
        wait_for_it=False,
    )
    industry_link.click()
    take_screenshot(driver, NAME + " after opening " + industry_name + " page")


def click_breadcrumb(driver: webdriver, name: str):
    breadcrumbs = find_elements(driver, by_css=BREADCRUMB_LINKS)
    url = driver.current_url
    link = None
    for breadcrumb in breadcrumbs:
        if breadcrumb.text.lower() == name.lower():
            link = breadcrumb
    assert link, "Couldn't find '{}' breadcrumb on {}".format(name, url)
    link.click()
    take_screenshot(driver, " after clicking on " + name + " breadcrumb")
