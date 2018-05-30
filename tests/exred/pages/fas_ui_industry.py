# -*- coding: utf-8 -*-
"""Find a Supplier - Generic Industry Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import (
    check_for_expected_sections_elements,
    check_for_section,
    check_title,
    check_url,
    go_to_url,
)
from settings import DIRECTORY_UI_SUPPLIER_URL
from utils import take_screenshot, find_element, assertion_msg

NAME = "Find a Supplier - Generic Industry page"
URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "industries/")
PAGE_TITLE = "trade.great.gov.uk"

INDUSTRY_BREADCRUMB = "p.breadcrumbs > span.current.bidi-rtl"
SECTIONS = {
    "hero": {
        "itself": "#hero",
        "header": "#hero h2",
        "description": "#hero p"
    },
    "breadcrumbs": {
        "itself": "#content p.breadcrumbs",
        "industry": INDUSTRY_BREADCRUMB
    },
    "contact us": {
        "itself": "#lede-section",
        "header": "#lede-section h2",
        "contact us": "#lede-section a"
    },
    "why choose UK industry": {
        "itself": "#lede-columns-section",
        "first": "#lede-columns-section div.column-one-third:nth-child(1)",
        "second": "#lede-columns-section div.column-one-third:nth-child(2)",
        "third": "#lede-columns-section div.column-one-third:nth-child(3)",
    },
    "companies": {
        "itself": "#companies-section",
        "header": "#companies-list-text h2",
        "search input": "#companies-section form > input[name=term]",
        "search button": "#companies-section form > button[type=submit]",
        "list of companies": "#companies-section ul",
        "view more": "#companies-section a.button",
    },
    "articles": {
        "itself": "#articles-section"
    },
}


def visit(driver: webdriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    check_title(driver, PAGE_TITLE, exact_match=False)
    check_for_expected_sections_elements(driver, SECTIONS)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_section(driver: webdriver, name: str):
    check_for_section(driver, SECTIONS, sought_section=name)


def should_see_content_for_industry(driver: webdriver, industry_name: str):
    industry_breadcrumb = find_element(
        driver, by_css=INDUSTRY_BREADCRUMB, element_name="Industry breadcrumb",
        wait_for_it=False)
    current_industry = industry_breadcrumb.text
    with assertion_msg(
            "Expected to see breadcrumb for '%s' industry but got '%s' instead"
            " on %s", industry_name, current_industry, driver.current_url):
        assert industry_name.lower() == current_industry.lower()
    source = driver.page_source
    with assertion_msg(
            "Expected to find term '%s' in the source of the page %s",
            industry_name, driver.current_url):
        assert industry_name.lower() in source.lower()
