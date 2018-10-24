# -*- coding: utf-8 -*-
"""great.gov.uk International EU Exit News Articles List page"""
import random
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    check_url,
    take_screenshot,
    check_for_sections,
    go_to_url,
    find_elements,
    find_and_click_on_page_element,
)
from settings import EXRED_UI_URL

NAME = "Updates for non-UK companies on EU Exit"
SERVICE = "Export Readiness"
TYPE = "international"
URL = urljoin(EXRED_UI_URL, "international/news/?lang=en")
PAGE_TITLE = ""


BETA_FEEDBACK = Selector(By.CSS_SELECTOR, "#header-beta-bar span > a")
SUBMIT_BUTTON = Selector(By.CSS_SELECTOR, "form button")
ARTICLES = Selector(By.CSS_SELECTOR, "li.article a")
SELECTORS = {
    "header": {
        "itself": Selector(By.ID, "international-header"),
        "skip": Selector(By.ID, "skip-link"),
        "header bar": Selector(By.ID, "international-header-bar"),
        "header menu": Selector(By.ID, "international-header-menu"),
        "logo": Selector(By.ID, "international-header-logo"),
    },
    "beta bar": {
        "itself": Selector(By.ID, "header-beta-bar"),
        "badge": Selector(By.CSS_SELECTOR, "#header-beta-bar .phase-tag"),
        "message": Selector(By.CSS_SELECTOR, "#header-beta-bar span"),
        "link": Selector(By.CSS_SELECTOR, "#header-beta-bar a"),
    },
    "hero": {
        "itself": Selector(By.ID, "hero"),
        "header": Selector(By.CSS_SELECTOR, "#hero h1"),
        "text": Selector(By.CSS_SELECTOR, "#hero p"),
    },
    "articles": {
        "itself": Selector(By.ID, "article-list-page"),
        "breadcrumbs": Selector(By.CSS_SELECTOR, "#article-list-page .breadcrumbs"),
        "great.gov.uk":
            Selector(
                By.CSS_SELECTOR, ".breadcrumbs a[href='/international/']"),
        "article list": Selector(By.CSS_SELECTOR, "ul.content-list"),
        "articles": Selector(By.CSS_SELECTOR, "li.article"),
        "article header": Selector(By.CSS_SELECTOR, "li.article h3"),
        "article text": Selector(By.CSS_SELECTOR, "li.article p"),
        "article link": ARTICLES,
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
    "footer": {
        "itself": Selector(By.ID, "international-footer"),
        "logo": Selector(By.ID, "international-footer-logo"),
        "share links": Selector(By.CSS_SELECTOR, "#international-footer ul"),
    }
}


def visit(driver: WebDriver, *, page_name: str = None, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def open_news_article(driver: WebDriver, article_number: int):
    article_links = find_elements(driver, ARTICLES)
    assert len(article_links) >= article_number
    article_links[article_number - 1].click()


def open_any_news_article(driver: WebDriver):
    article_links = find_elements(driver, ARTICLES)
    assert len(article_links) > 0
    article_links[random.randint(1, len(article_links)) - 1].click()


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)
