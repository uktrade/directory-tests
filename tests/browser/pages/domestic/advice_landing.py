# -*- coding: utf-8 -*-
"""ExRed Common Advice Page Object."""
import random
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Selector,
    check_for_sections,
    check_if_element_is_visible,
    check_url,
    find_elements,
    go_to_url,
    take_screenshot,
    wait_for_page_load_after_action,
)
from settings import EXRED_UI_URL

NAME = "Advice landing"
TYPE = "landing"
SERVICE = "Export Readiness"
URL = urljoin(EXRED_UI_URL, "advice/")
PAGE_TITLE = "Welcome to great.gov.uk"

ARTICLE_LINKS = Selector(
    By.CSS_SELECTOR,
    "#content section.topic-list-section div.card a",
    type=ElementType.LINK,
)
SELECTORS = {
    "hero": {
        "itself": Selector(By.CSS_SELECTOR, "section.hero"),
        "heading": Selector(By.ID, "hero-heading"),
    },
    "breadcrumbs": {
        "itself": Selector(By.CSS_SELECTOR, "nav.breadcrumbs"),
        "links": Selector(By.CSS_SELECTOR, "nav.breadcrumbs a"),
    },
    "advice & guidance tiles": {
        "itself": Selector(By.CSS_SELECTOR, "div.card-grid"),
        "cards": Selector(By.CSS_SELECTOR, "section.topic-list-section div.card"),
        "articles": ARTICLE_LINKS,
    },
    "error reporting": {
        "itself": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "link": Selector(By.ID, "error-reporting-section-contact-us"),
    },
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, PAGE_TITLE)
    check_url(driver, URL, exact_match=False)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def extract_text(text: str) -> tuple:
    advice_name_index = 1
    article_counter_index = -2
    name = text.splitlines()[advice_name_index]
    counter = int(text.split()[article_counter_index])
    return name, counter


def open_any_article(driver: WebDriver) -> tuple:
    article_links = find_elements(driver, ARTICLE_LINKS)
    link = random.choice(article_links)
    link_text = link.text
    check_if_element_is_visible(link, element_name=link_text)
    with wait_for_page_load_after_action(driver):
        link.click()
    return extract_text(link_text)
