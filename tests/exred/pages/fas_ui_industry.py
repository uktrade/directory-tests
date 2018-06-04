# -*- coding: utf-8 -*-
"""Find a Supplier - Generic Industry Page Object."""
import logging
from enum import Enum
from urllib.parse import urljoin

from selenium import webdriver
from utils import assertion_msg, find_element, find_elements, take_screenshot

from pages.common_actions import (
    check_for_expected_sections_elements,
    check_for_section,
    check_title,
    check_url,
    find_and_click_on_page_element,
    go_to_url
)
from settings import DIRECTORY_UI_SUPPLIER_URL

BASE_URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "industries/")


class URLS(Enum):
    """Lists all URLs for industry page."""
    AEROSPACE = urljoin(BASE_URL, "aerospace/")
    AGRITECH = urljoin(BASE_URL, "agritech/")
    AUTOMOTIVE = urljoin(BASE_URL, "automotive/")
    BUSINESS_AND_GOVERNMENT_PARTNERSHIPS = urljoin(BASE_URL, "business-and-government-partnerships/")
    CONSUMER_RETAIL = urljoin(BASE_URL, "consumer-retail/")
    CREATIVE_SERVICES = urljoin(BASE_URL, "creative-services/")
    CYBER_SECURITY = urljoin(BASE_URL, "cyber-security/")
    EDUCATION = urljoin(BASE_URL, "education-industry/")
    ENERGY = urljoin(BASE_URL, "energy/")
    ENGINEERING = urljoin(BASE_URL, "engineering-industry/")
    FOOD_AND_DRINK = urljoin(BASE_URL, "food-and-drink/")
    HEALTHCARE = urljoin(BASE_URL, "healthcare/")
    INFRASTRUCTURE = urljoin(BASE_URL, "infrastructure/")
    INNOVATION = urljoin(BASE_URL, "innovation-industry/")
    LEGAL_SERVICES = urljoin(BASE_URL, "legal-services/")
    LIFE_SCIENCES = urljoin(BASE_URL, "life-sciences/")
    MARINE = urljoin(BASE_URL, "marine/")
    PROFESSIONAL_AND_FINANCIAL_SERVICES = urljoin(BASE_URL, "professional-and-financial-services/")
    SPACE = urljoin(BASE_URL, "space/")
    SPORTS_ECONOMY = urljoin(BASE_URL, "sports-economy/")
    TECHNOLOGY = urljoin(BASE_URL, "technology/")


NAME = "Find a Supplier - Generic Industry page"
URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "industries/")
PAGE_TITLE = "trade.great.gov.uk"

BREADCRUMB_LINKS = "p.breadcrumbs > a"
INDUSTRY_BREADCRUMB = "p.breadcrumbs > span.current.bidi-rtl"
SEARCH_INPUT = "#companies-section form > input[name=term]"
SEARCH_BUTTON = "#companies-section form > button[type=submit]"
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
    "selling points": {
        "itself": "#lede-columns-section",
        "first": "#lede-columns-section div.column-one-third:nth-child(1)",
        "second": "#lede-columns-section div.column-one-third:nth-child(2)",
        "third": "#lede-columns-section div.column-one-third:nth-child(3)",
    },
    "search for uk suppliers": {
        "itself": "#companies-section",
        "header": "#companies-list-text h2",
        "search input": SEARCH_INPUT,
        "search button": SEARCH_BUTTON,
        "list of companies": "#companies-section ul",
        "view more": "#companies-section a.button",
    },
    "articles": {
        "itself": "#articles-section"
    },
}


def visit(
        driver: webdriver, *, first_time: bool = False, page_name: str = None):
    if page_name:
        enum_key = page_name.lower()\
            .replace("fas ", "").replace(" industry", "").replace(" ", "_")\
            .replace("-", "_").upper()
        url = URLS[enum_key].value
    else:
        url = URL
    go_to_url(driver, url, NAME, first_time=first_time)


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


def click_on_page_element(driver: webdriver, element_name: str):
    find_and_click_on_page_element(driver, SECTIONS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)


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


def search(driver: webdriver, *, keyword: str = None, sector: str = None):
    """
    sector is not used, but kept for compatibility with search() in other POs.
    """
    input_field = find_element(
        driver, by_css=SEARCH_INPUT, element_name="Search input field",
        wait_for_it=False)
    input_field.clear()
    if keyword:
        input_field.send_keys(keyword)
    take_screenshot(driver, NAME + " after entering the keyword")
    button = find_element(
        driver, by_css=SEARCH_BUTTON, element_name="Search button",
        wait_for_it=False)
    button.click()
    take_screenshot(driver, NAME + " after submitting the search form")
