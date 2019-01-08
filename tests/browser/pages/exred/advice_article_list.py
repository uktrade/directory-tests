# -*- coding: utf-8 -*-
"""ExRed Common Advice Page Object."""
import logging
import random
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    check_for_sections,
    check_if_element_is_visible,
    check_url,
    find_element,
    find_elements,
    get_selectors,
    go_to_url,
    Selector,
    take_screenshot,
    wait_for_page_load_after_action,
)
from settings import EXRED_UI_URL

NAME = "Advice"
TYPE = "article list"
SERVICE = "Export Readiness"
URL = urljoin(EXRED_UI_URL, "advice/")
PAGE_TITLE = "Welcome to great.gov.uk"
NAMES = [
    "Create an export plan",
    "Find an export market",
    "Define route to market",
    "Get export finance and funding",
    "Manage payment for export orders",
    "Prepare to do business in a foreign country",
    "Manage legal and ethical compliance",
    "Prepare for export procedures and logistics",
]
URLs = {
    "create an export plan": urljoin(URL, "create-an-export-plan/"),
    "find an export market": urljoin(URL, "find-an-export-market/"),
    "define route to market": urljoin(URL, "define-route-to-market/"),
    "get export finance and funding": urljoin(URL, "get-export-finance-and-funding/"),
    "manage payment for export orders": urljoin(URL, "manage-payment-for-export-orders/"),
    "prepare to do business in a foreign country": urljoin(URL, "prepare-to-do-business-in-a-foreign-country/"),
    "manage legal and ethical compliance": urljoin(URL, "manage-legal-and-ethical-compliance/"),
    "prepare for export procedures and logistics": urljoin(URL, "prepare-for-export-procedures-and-logistics/"),
}


TOTAL_NUMBER_OF_ARTICLES = Selector(By.CSS_SELECTOR, "dd.position > span.to")
ARTICLES_TO_READ_COUNTER = Selector(By.CSS_SELECTOR, "dd.position > span.from")
TIME_TO_COMPLETE = Selector(By.CSS_SELECTOR, "dd.time > span.value")
ARTICLES_LIST = Selector(By.CSS_SELECTOR, "#js-paginate-list > li")
FIRST_ARTICLE = Selector(By.CSS_SELECTOR, "#js-paginate-list > li:nth-child(1) > a")

ARTICLE_COUNTER = Selector(By.ID, "hero-description")
ARTICLE_LINKS = Selector(
    By.CSS_SELECTOR, "#article-list-page li.article a", type=ElementType.LINK)
SELECTORS = {
    "hero": {
        "itself": Selector(By.ID, "hero"),
        "heading": Selector(By.ID, "hero-heading"),
        "description": Selector(By.ID, "hero-description"),
    },
    "breadcrumbs": {
        "itself": Selector(By.CSS_SELECTOR, "nav.breadcrumbs"),
        "links": Selector(By.CSS_SELECTOR, "nav.breadcrumbs a"),
    },
    "total number of articles": {
        "itself": ARTICLE_COUNTER,
    },
    "list of articles": {
        "itself": Selector(By.ID, "article-list-page"),
        "articles": ARTICLE_LINKS,
    },
    "error reporting": {
        "itself": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "link": Selector(By.ID, "error-reporting-section-contact-us"),
    },
}


def clean_name(name: str) -> str:
    return name.split(" - ")[1].strip()


def visit(driver: WebDriver, *, page_name: str = None):
    if page_name:
        key = clean_name(page_name).lower()
        url = URLs[key]
    else:
        url = URL
    go_to_url(driver, url, NAME)


def should_be_here(driver: WebDriver, *, page_name: str):
    take_screenshot(driver, PAGE_TITLE)
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def get_article_counter(driver: WebDriver) -> int:
    article_counter = find_element(
        driver, ARTICLE_COUNTER, element_name="total number of articles",
        wait_for_it=False
    )
    counter_index = 0
    return int(article_counter.text.split()[counter_index])


def article_counter_is_equal_to(driver: WebDriver, expected_article_counter: int):
    current_counter = get_article_counter(driver)
    error = (f"Expected Advice article counter to be "
             f"{expected_article_counter} but found {current_counter} on "
             f"{driver.current_url}")
    assert current_counter == expected_article_counter, error


def article_counter_matches_number_of_articles(driver: WebDriver):
    current_counter = get_article_counter(driver)
    article_links = find_elements(driver, ARTICLE_LINKS)
    error = (f"Expected Advice article counter ({current_counter}) to match "
             f"number of visible articles {len(article_links)} on"
             f"{driver.current_url}")
    assert current_counter == len(article_links), error


def open_any_article(driver: WebDriver) -> str:
    article_links = find_elements(driver, ARTICLE_LINKS)
    link = random.choice(article_links)
    link_text = link.text
    check_if_element_is_visible(link, element_name=link_text)
    with wait_for_page_load_after_action(driver):
        link.click()
    return link_text


def extract_text(text: str, section_name: str) -> tuple:
    if section_name.lower() == "advice":
        advice_name_index = 1
        article_counter_index = -2
        name = text.splitlines()[advice_name_index]
        counter = int(text.split()[article_counter_index])
        return name, counter


def open_any_element_in_section(
        driver: WebDriver, element_type: str, section_name: str) -> tuple:
    section = SELECTORS[section_name.lower()]
    sought_type = ElementType[element_type.upper()]
    selectors = get_selectors(section, sought_type)
    error = f"Could't find any {element_type} in {section_name} section"
    assert len(selectors) > 0, error
    selector_key = random.choice(list(selectors))
    selector = SELECTORS[section_name.lower()][selector_key]
    elements = find_elements(driver, selector)
    element = random.choice(elements)
    check_if_element_is_visible(element, element_name=selector_key)
    element_text = extract_text(element.text, section_name)
    with wait_for_page_load_after_action(driver):
        element.click()
    return element_text
