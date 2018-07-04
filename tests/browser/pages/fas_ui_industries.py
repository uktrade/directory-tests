# -*- coding: utf-8 -*-
"""Find a Supplier - Industries Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver
from utils import find_element, find_elements, take_screenshot

from pages.common_actions import (
    check_for_expected_sections_elements,
    check_for_section,
    check_title,
    check_url,
    find_and_click_on_page_element,
    go_to_url,
)
from settings import DIRECTORY_UI_SUPPLIER_URL

NAME = "Find a Supplier - Industries page"
URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "industries/")
PAGE_TITLE = (
    "Find the best UK suppliers for your industry - trade.great.gov.uk"
)

BREADCRUMB_LINKS = "p.breadcrumbs > a"
INDUSTRIES_BREADCRUMB = "p.breadcrumbs > span.current.bidi-rtl"
INDUSTRIES_LINKS = "#industry-pages-container > section a"
MORE_INDUSTRIES_LINKS = "#industry-pages-container > ul a"
SECTIONS = {
    "hero": {"itself": "#hero", "header": "#hero h1"},
    "breadcrumbs": {
        "itself": "#content p.breadcrumbs",
        "industries": INDUSTRIES_BREADCRUMB,
    },
    "contact us": {
        "itself": "#introduction",
        "header": "#introduction p",
        "contact us": "#introduction a",
    },
    "industries": {
        "itself": "#industry-pages-container",
        "industries": INDUSTRIES_LINKS,
    },
    "more industries": {
        "itself": "#industry-pages-container > ul",
        "more industries": MORE_INDUSTRIES_LINKS,
    },
}


def visit(driver: webdriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    check_title(driver, PAGE_TITLE, exact_match=True)
    check_for_expected_sections_elements(driver, SECTIONS)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_section(driver: webdriver, name: str):
    check_for_section(driver, SECTIONS, sought_section=name)


def click_on_page_element(driver: webdriver, element_name: str):
    find_and_click_on_page_element(driver, SECTIONS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)


def clean_name(name: str) -> str:
    return name.replace("FAS", "").replace("industry", "").strip()


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
