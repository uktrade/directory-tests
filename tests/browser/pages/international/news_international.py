# -*- coding: utf-8 -*-
"""great.gov.uk International EU Exit News Articles List page"""
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import common_selectors
from pages.common_actions import (
    Selector,
    check_for_sections,
    check_url,
    find_elements,
    go_to_url,
)

NAME = "Updates for non UK companies on EU Exit"
SERVICE = Service.INTERNATIONAL
TYPE = PageType.CONTENT
URL = URLs.INTERNATIONAL_BREXIT_NEWS.absolute
PAGE_TITLE = ""

SUBMIT_BUTTON = Selector(By.CSS_SELECTOR, "form[method=POST] button")
ARTICLES = Selector(By.CSS_SELECTOR, "li.article a")
SELECTORS = {
    "hero": {
        "itself": Selector(By.ID, "hero"),
        "header": Selector(By.CSS_SELECTOR, "#hero h1"),
        "text": Selector(By.CSS_SELECTOR, "#hero p"),
    },
    "articles": {
        "itself": Selector(By.ID, "article-list-page"),
        "breadcrumbs": Selector(By.CSS_SELECTOR, "#article-list-page .breadcrumbs"),
        "great.gov.uk": Selector(
            By.CSS_SELECTOR, ".breadcrumbs a[href='/international/']"
        ),
        "article list": Selector(By.CSS_SELECTOR, "ul.content-list"),
        "articles": Selector(By.CSS_SELECTOR, "li.article"),
        "article header": Selector(By.CSS_SELECTOR, "li.article h3"),
        "article text": Selector(By.CSS_SELECTOR, "li.article p"),
        "article link": ARTICLES,
    },
    "contact us": {
        "itself": Selector(By.ID, "eu-exit-cta-box"),
        "description": Selector(By.CSS_SELECTOR, "#eu-exit-cta-box p"),
        "contact us": Selector(By.CSS_SELECTOR, "#eu-exit-cta-box a"),
    },
}
SELECTORS.update(common_selectors.INTERNATIONAL_HEADER)
SELECTORS.update(common_selectors.BETA_BAR)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.INTERNATIONAL_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=False)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def open_news_article(driver: WebDriver, article_number: int):
    article_links = find_elements(driver, ARTICLES)
    assert len(article_links) >= article_number
    article_links[article_number - 1].click()
