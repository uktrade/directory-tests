# -*- coding: utf-8 -*-
"""Find a Supplier - Generic Industry Page Object."""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import common_selectors
from pages.common_actions import (
    Selector,
    assertion_msg,
    check_for_sections,
    check_url,
    find_element,
    go_to_url,
    take_screenshot,
)

NAME = "Industry"
NAMES = [
    "Aerospace",
    "Agritech",
    "Automotive",
    "Business & Government Partnerships",
    "Consumer & retail",
    "Creative industries",
    "Creative services",
    "Cyber security",
    "Education",
    "Energy",
    "Engineering",
    "Engineering and manufacturing",
    "Food and drink",
    "Financial and professional services",
    "Healthcare",
    "Infrastructure",
    "Innovation",
    "Legal services",
    "Life sciences",
    "Marine",
    "Professional & financial services",
    "Space",
    "Sports economy",
    "Technology",
]
SERVICE = Service.FAS
TYPE = PageType.INDUSTRY
URL = URLs.FAS_INDUSTRIES.absolute
PAGE_TITLE = "trade.great.gov.uk"

COMPANY_PROFILE_LINK = "#companies-section li:nth-child({number}) a.link"
ARTICLE_LINK = "#articles-section article:nth-child({number}) a"

BREADCRUMB_LINKS = Selector(By.CSS_SELECTOR, "p.breadcrumbs > a")
INDUSTRY_BREADCRUMB = Selector(By.CSS_SELECTOR, "p.breadcrumbs > span.current")
SEARCH_INPUT = Selector(By.CSS_SELECTOR, "#companies-section form > input[name=term]")
SEARCH_BUTTON = Selector(
    By.CSS_SELECTOR, "#companies-section form > button[type=submit]"
)
SELECTORS = {
    "hero": {
        "itself": Selector(By.ID, "hero"),
        "header": Selector(By.CSS_SELECTOR, "#hero h2"),
        "description": Selector(By.CSS_SELECTOR, "#hero p"),
    },
    "breadcrumbs": {
        "itself": Selector(By.CSS_SELECTOR, "#content p.breadcrumbs"),
        "industry": INDUSTRY_BREADCRUMB,
    },
    "contact us": {
        "itself": Selector(By.ID, "lede-section"),
        "header": Selector(By.CSS_SELECTOR, "#lede-section h2"),
        "contact us": Selector(By.CSS_SELECTOR, "#lede-section a"),
    },
    "selling points": {
        "itself": Selector(By.ID, "lede-columns-section"),
        "first": Selector(
            By.CSS_SELECTOR, "#lede-columns-section div.column-one-third:nth-child(1)"
        ),
        "second": Selector(
            By.CSS_SELECTOR, "#lede-columns-section div.column-one-third:nth-child(2)"
        ),
        "third": Selector(
            By.CSS_SELECTOR, "#lede-columns-section div.column-one-third:nth-child(3)"
        ),
    },
    "search for uk suppliers": {
        "itself": Selector(By.ID, "companies-section"),
        "header": Selector(By.CSS_SELECTOR, "#companies-list-text h2"),
        "search input": SEARCH_INPUT,
        "search button": SEARCH_BUTTON,
        "list of companies": Selector(By.CSS_SELECTOR, "#companies-section ul"),
        "view more": Selector(By.CSS_SELECTOR, "#companies-section a.button"),
    },
    "articles": {"itself": Selector(By.ID, "articles-section")},
}
SELECTORS.update(common_selectors.INTERNATIONAL_HEADER_WO_LANGUAGE_SELECTOR)
SELECTORS.update(common_selectors.INTERNATIONAL_FOOTER)

SubURLs = {
    "aerospace": urljoin(URL, "aerospace/"),
    "agritech": urljoin(URL, "agritech/"),
    "automotive": urljoin(URL, "automotive/"),
    "business & government partnerships": urljoin(
        URL, "business-and-government-partnerships/"
    ),
    "consumer & retail": urljoin(URL, "consumer-retail/"),
    "creative industries": urljoin(URL, "creative-industries/"),
    "creative services": urljoin(URL, "creative-services/"),
    "cyber security": urljoin(URL, "cyber-security/"),
    "education": urljoin(URL, "education-industry/"),
    "energy": urljoin(URL, "energy/"),
    "engineering": urljoin(URL, "engineering-industry/"),
    "engineering and manufacturing": urljoin(URL, "engineering-and-manufacturing/"),
    "financial and professional services": urljoin(URL, "financial-services/"),
    "food and drink": urljoin(URL, "food-and-drink/"),
    "healthcare": urljoin(URL, "healthcare/"),
    "infrastructure": urljoin(URL, "infrastructure/"),
    "innovation": urljoin(URL, "innovation-industry/"),
    "legal services": urljoin(URL, "legal-services/"),
    "life sciences": urljoin(URL, "life-sciences/"),
    "marine": urljoin(URL, "marine/"),
    "professional & financial services": urljoin(
        URL, "professional-and-financial-services/"
    ),
    "space": urljoin(URL, "space/"),
    "sports economy": urljoin(URL, "sports-economy/"),
    "technology": urljoin(URL, "technology/"),
}


def clean_name(name: str) -> str:
    return name.split(" - ")[1].strip()


def visit(driver: WebDriver, *, page_name: str = None):
    url = SubURLs[page_name] if page_name else URL
    go_to_url(driver, url, NAME)


def should_be_here(driver: WebDriver, *, page_name: str):
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def should_see_content_for(driver: WebDriver, industry_name: str):
    industry_name = clean_name(industry_name)
    logging.debug("Looking for: {}".format(industry_name))
    industry_breadcrumb = find_element(
        driver,
        INDUSTRY_BREADCRUMB,
        element_name="Industry breadcrumb",
        wait_for_it=False,
    )
    current_industry = industry_breadcrumb.text
    with assertion_msg(
        "Expected to see breadcrumb for '%s' industry but got '%s' instead" " on %s",
        industry_name,
        current_industry,
        driver.current_url,
    ):
        assert industry_name == current_industry
    source = driver.page_source
    with assertion_msg(
        "Expected to find term '%s' in the source of the page %s",
        industry_name,
        driver.current_url,
    ):
        from html import escape

        assert escape(industry_name) in source


def search(driver: WebDriver, *, keyword: str = None, sector: str = None):
    """
    sector is not used, but kept for compatibility with search() in other POs.
    """
    input_field = find_element(
        driver, SEARCH_INPUT, element_name="Search input field", wait_for_it=False
    )
    input_field.clear()
    if keyword:
        input_field.send_keys(keyword)
    take_screenshot(driver, NAME + " after entering the keyword")
    button = find_element(
        driver, SEARCH_BUTTON, element_name="Search button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, NAME + " after submitting the search form")


def open_profile(driver: WebDriver, number: int):
    selector = Selector(By.CSS_SELECTOR, COMPANY_PROFILE_LINK.format(number=number))
    link = find_element(driver, selector)
    link.click()
    take_screenshot(driver, NAME + " after clicking on company profile link")


def open_article(driver: WebDriver, number: int):
    selector = Selector(By.CSS_SELECTOR, ARTICLE_LINK.format(number=number))
    link = find_element(driver, selector)
    if link.get_attribute("target") == "_blank":
        href = link.get_attribute("href")
        driver.get(href)
    else:
        link.click()
    take_screenshot(driver, NAME + " after clicking on article link")
