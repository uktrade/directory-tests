# -*- coding: utf-8 -*-
"""great.gov.uk Search by Tag results page"""
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    check_for_sections,
    check_url,
    find_element,
    take_screenshot,
)
from settings import EXRED_UI_URL

NAME = "Search by tag"
SERVICE = "Export Readiness"
TYPE = "search"
URL = urljoin(EXRED_UI_URL, "prototype/tagged/")
PAGE_TITLE = ""

HERO_HEADING = Selector(By.ID, "hero-heading")
SELECTORS = {
    "hero": {
        "itself": Selector(By.CSS_SELECTOR, "#content > section.hero"),
        "heading": HERO_HEADING,
        "counter": Selector(By.CSS_SELECTOR, "section.hero p"),
    },
    "article list": {
        "itself": Selector(By.ID, "article-list-page"),
        "breadcrumbs": Selector(By.CSS_SELECTOR, "div.breadcrumbs"),
        "news": Selector(By.CSS_SELECTOR, "#article-list-page ul li"),
        "links": Selector(By.CSS_SELECTOR, "#article-list-page ul li a"),
        "last updated dates": Selector(By.CSS_SELECTOR, "#article-list-page ul li p"),
    },
    "error reporting": {
        "itself": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "link": Selector(By.ID, "error-reporting-section-contact-us"),
    },
}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)


def is_filtered_by_tag(driver: WebDriver, tag: str):
    heading = find_element(driver, HERO_HEADING)
    clean_tag = tag.replace(" ", "-").upper()
    error = (
        f"Expected to see tag: '{clean_tag}' in page heading but got "
        f"'{heading.text}' instead"
    )
    assert clean_tag in heading.text.upper(), error


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)
