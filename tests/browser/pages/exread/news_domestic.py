# -*- coding: utf-8 -*-
"""great.gov.uk Domestic EU Exit News Article page"""
import random
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    check_url,
    take_screenshot,
    go_to_url,
    find_elements,
    find_and_click_on_page_element,
    check_for_sections
)
from settings import EXRED_UI_URL

NAME = "Updates for UK companies on EU Exit"
SERVICE = "Export Readiness"
TYPE = "Domestic"
URL = urljoin(EXRED_UI_URL, "eu-exit-news/")
PAGE_TITLE = "Welcome to great.gov.uk"


ARTICLES = Selector(By.CSS_SELECTOR, "#news-list-page ul li a")
SELECTORS = {
    "header bar": {"itself": Selector(By.ID, "header-bar")},
    "header menu": {
        "itself": Selector(By.ID, "header-menu"),
        "logo": Selector(By.CSS_SELECTOR, "#header-dit-logo img"),
    },
    "hero": {
        "itself": Selector(By.CSS_SELECTOR, "#content > section.hero"),
        "heading": Selector(By.ID, "hero-heading"),
        "counter": Selector(By.CSS_SELECTOR, "section.hero p"),
    },
    "articles": {
        "itself": Selector(By.ID, "news-list-page"),
        "breadcrumbs": Selector(By.CSS_SELECTOR, "div.breadcrumbs"),
        "news": Selector(By.CSS_SELECTOR, "#news-list-page ul li"),
        "articles": ARTICLES,
        "last updated dates": Selector(
            By.CSS_SELECTOR, "#news-list-page ul li p"
        ),
    },
    "call to action": {
        "itself": Selector(By.CSS_SELECTOR, "div.cta-box"),
        "description": Selector(By.CSS_SELECTOR, "div.cta-box p"),
        "contact us": Selector(By.CSS_SELECTOR, "div.cta-box a"),
    },
    "error reporting": {
        "itself": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "link": Selector(By.ID, "error-reporting-section-contact-us"),
    },
}


def visit(driver: WebDriver, *, page_name: str = None, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def open_any_news_article(driver: WebDriver):
    article_links = find_elements(driver, ARTICLES)
    assert len(article_links) > 0
    article_links[random.randint(1, len(article_links)) - 1].click()


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)
