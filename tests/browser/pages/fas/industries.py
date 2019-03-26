# -*- coding: utf-8 -*-
"""Find a Supplier - Industries Page Object."""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    check_for_sections,
    check_url,
    find_and_click_on_page_element,
    find_element,
    find_elements,
    go_to_url,
    take_screenshot,
)
from settings import DIRECTORY_UI_SUPPLIER_URL

NAME = "Industries"
SERVICE = "Find a Supplier"
TYPE = "industries"
URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "industries/")
PAGE_TITLE = "Find the best UK suppliers for your industry - trade.great.gov.uk"

BREADCRUMB_LINKS = Selector(By.CSS_SELECTOR, "p.breadcrumbs > a")
INDUSTRIES_BREADCRUMB = Selector(By.CSS_SELECTOR, "p.breadcrumbs > span.current")
INDUSTRIES_LINKS = Selector(By.CSS_SELECTOR, "#industry-pages-container > section a")
MORE_INDUSTRIES_LINKS = Selector(By.CSS_SELECTOR, "#industry-pages-container > ul a")
SELECTORS = {
    "hero": {
        "itself": Selector(By.ID, "hero"),
        "header": Selector(By.CSS_SELECTOR, "#hero h1"),
    },
    "breadcrumbs": {
        "itself": Selector(By.CSS_SELECTOR, "#content p.breadcrumbs"),
        "industries": INDUSTRIES_BREADCRUMB,
    },
    "contact us": {
        "itself": Selector(By.ID, "introduction"),
        "header": Selector(By.CSS_SELECTOR, "#introduction p"),
        "contact us": Selector(By.CSS_SELECTOR, "#introduction a"),
    },
    "industries": {
        "itself": Selector(By.ID, "industry-pages-container"),
        "industries": INDUSTRIES_LINKS,
    },
    "more industries": {
        "itself": Selector(By.CSS_SELECTOR, "#industry-pages-container > ul"),
        "more industries": MORE_INDUSTRIES_LINKS,
    },
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)


def open_industry(driver: WebDriver, industry_name: str):
    industry_name = industry_name.split(" - ")[1].strip()
    selector = Selector(By.LINK_TEXT, industry_name)
    logging.debug("Looking for: {}".format(industry_name))
    industry_link = find_element(
        driver, selector, element_name="Industry card", wait_for_it=False
    )
    industry_link.click()
    take_screenshot(driver, NAME + " after opening " + industry_name + " page")


def click_breadcrumb(driver: WebDriver, name: str):
    breadcrumbs = find_elements(driver, BREADCRUMB_LINKS)
    url = driver.current_url
    link = None
    for breadcrumb in breadcrumbs:
        if breadcrumb.text.lower() == name.lower():
            link = breadcrumb
    assert link, "Couldn't find '{}' breadcrumb on {}".format(name, url)
    link.click()
    take_screenshot(driver, " after clicking on " + name + " breadcrumb")
