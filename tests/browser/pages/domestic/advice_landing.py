# -*- coding: utf-8 -*-
"""Domestic Common Advice Page Object."""
import random
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType, common_selectors
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

NAME = "Advice landing"
TYPE = PageType.LANDING
SERVICE = Service.DOMESTIC
URL = URLs.DOMESTIC_ADVICE.absolute
PAGE_TITLE = "Welcome to great.gov.uk"

ARTICLE_LINKS = Selector(
    By.CSS_SELECTOR, "#advice-list-section a", type=ElementType.LINK
)
SELECTORS = {
    "advice & guidance tiles": {
        "itself": Selector(By.ID, "advice-list-section"),
        "cards": Selector(By.CSS_SELECTOR, "#advice-list-section div.card"),
        "articles": ARTICLE_LINKS,
        "article images": Selector(By.CSS_SELECTOR, "#advice-list-section .card-image"),
    }
}
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.INTERNATIONAL_HERO)
SELECTORS.update(common_selectors.ERROR_REPORTING)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, PAGE_TITLE)
    check_url(driver, URL, exact_match=False)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def open_any_article(driver: WebDriver) -> str:
    article_links = find_elements(driver, ARTICLE_LINKS)
    link = random.choice(article_links)
    link_text = link.text
    check_if_element_is_visible(link, element_name=link_text)
    with wait_for_page_load_after_action(driver):
        link.click()
    return link_text
