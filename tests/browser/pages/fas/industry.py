# -*- coding: utf-8 -*-
"""Find a Supplier - Generic Industry Page Object."""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    AssertionExecutor,
    Selector,
    assertion_msg,
    check_for_expected_sections_elements,
    check_for_sections,
    check_title,
    check_url,
    find_and_click_on_page_element,
    find_element,
    find_elements,
    go_to_url,
    take_screenshot,
)
from settings import DIRECTORY_UI_SUPPLIER_URL

NAME = "Industry"
NAMES = [
    "Aerospace",
    "Agritech",
    "Consumer retail",
    "Creative services",
    "Cyber security",
    "Food and drink",
    "Healthcare",
    "Life sciences",
    "Sports economy",
    "Technology",
    "Legal services",
]
SERVICE = "Find a Supplier"
TYPE = "industry"
URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "industries/")
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

URLs = {
    "aerospace": urljoin(URL, "aerospace/"),
    "agritech": urljoin(URL, "agritech/"),
    "automotive": urljoin(URL, "automotive/"),
    "business and government partnerships": urljoin(URL, "business-and-government-partnerships/"),
    "consumer retail": urljoin(URL, "consumer-retail/"),
    "creative services": urljoin(URL, "creative-services/"),
    "cyber security": urljoin(URL, "cyber-security/"),
    "education": urljoin(URL, "education-industry/"),
    "energy": urljoin(URL, "energy/"),
    "engineering": urljoin(URL, "engineering-industry/"),
    "food and drink": urljoin(URL, "food-and-drink/"),
    "healthcare": urljoin(URL, "healthcare/"),
    "infrastructure": urljoin(URL, "infrastructure/"),
    "innovation": urljoin(URL, "innovation-industry/"),
    "legal services": urljoin(URL, "legal-services/"),
    "life sciences": urljoin(URL, "life-sciences/"),
    "marine": urljoin(URL, "marine/"),
    "professional and financial services": urljoin(URL, "professional-and-financial-services/"),
    "space": urljoin(URL, "space/"),
    "sports economy": urljoin(URL, "sports-economy/"),
    "technology": urljoin(URL, "technology/"),
}


def clean_name(name: str) -> str:
    return name.split(" - ")[1].strip()


def visit(driver: WebDriver, *, first_time: bool = False, page_name: str = None):
    key = clean_name(page_name).lower()
    url = URLs[key]
    go_to_url(driver, url, NAME, first_time=first_time)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    check_title(driver, PAGE_TITLE, exact_match=False)
    check_for_expected_sections_elements(driver, SELECTORS)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(executor: AssertionExecutor, names: List[str]):
    check_for_sections(executor, all_sections=SELECTORS, sought_sections=names)


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
        assert industry_name in source


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)


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
