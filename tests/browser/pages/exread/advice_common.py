# -*- coding: utf-8 -*-
"""ExRed Common Advice Page Object."""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Selector,
    check_if_element_is_visible,
    find_element,
    find_elements,
    take_screenshot,
    wait_for_page_load_after_action,
    check_url,
    check_for_sections
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


def should_be_here(driver: WebDriver, *, page_name: str):
    take_screenshot(driver, PAGE_TITLE)
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def open_first_article(driver: WebDriver):
    first_article = find_element(
        driver, FIRST_ARTICLE, element_name="First article on list",
        wait_for_it=False
    )
    check_if_element_is_visible(
        first_article, element_name="First article on list")
    with wait_for_page_load_after_action(driver):
        first_article.click()
    take_screenshot(driver, "after opening first article")
