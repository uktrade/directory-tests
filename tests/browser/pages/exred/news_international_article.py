# -*- coding: utf-8 -*-
"""great.gov.uk International EU Exit News Article page"""
import random
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    check_url,
    find_and_click_on_page_element,
    find_elements,
    take_screenshot,
)
from settings import EXRED_UI_URL

NAME = "International EU Exit news"
SERVICE = "Export Readiness"
TYPE = "article"
URL = urljoin(EXRED_UI_URL, "international/eu-exit-news/")
PAGE_TITLE = ""


TAGS = Selector(By.CSS_SELECTOR, "ul.tag-list a")
RELATED_ARTICLES = Selector(
    By.CSS_SELECTOR, "#article > article > div > div > div.column-quarter ul a"
)
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
    "share menu": {
        "itself": Selector(By.CSS_SELECTOR, "ul.sharing-links"),
        "twitter": Selector(By.ID, "share-twitter"),
        "facebook": Selector(By.ID, "share-facebook"),
        "linkedin": Selector(By.ID, "share-linkedin"),
        "email": Selector(By.ID, "share-email"),
    },
    "article": {
        "itself": Selector(By.ID, "article"),
        "breadcrumbs": Selector(By.CSS_SELECTOR, ".breadcrumbs"),
        "great.gov.uk": Selector(
            By.CSS_SELECTOR, ".breadcrumbs a[href='/international/']"
        ),
        "updates for non-uk companies on eu exit": Selector(
            By.CSS_SELECTOR, ".breadcrumbs a[href='/international/eu-exit-news/']"
        ),
        "header": Selector(By.CSS_SELECTOR, "#article h1"),
        "lede": Selector(By.CSS_SELECTOR, "#article p.lede"),
        "updates for companies on eu exit": Selector(
            By.CSS_SELECTOR, "article footer nav > div:nth-child(1) a"
        ),
        "back to top": Selector(
            By.CSS_SELECTOR, "article footer nav > div:nth-child(2) a"
        ),
    },
    "tag list": {"itself": Selector(By.CSS_SELECTOR, "ul.tag-list"), "tags": TAGS},
    "related content": {
        "itself": Selector(
            By.CSS_SELECTOR, "#article > article > div > div > div.column-quarter"
        ),
        "related articles": RELATED_ARTICLES,
    },
    "error reporting": {
        "itself": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "link": Selector(By.ID, "error-reporting-section-contact-us"),
    },
    "footer": {
        "itself": Selector(By.ID, "international-footer"),
        "logo": Selector(By.ID, "international-footer-logo"),
        "share links": Selector(By.CSS_SELECTOR, "#international-footer ul"),
    },
}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)


def open_any_tag(driver: WebDriver) -> str:
    links = find_elements(driver, TAGS)
    assert len(links) > 0
    link = links[random.randint(1, len(links)) - 1]
    tag = link.text.lower()
    link.click()
    return tag


def open_any_related_article(driver: WebDriver):
    links = find_elements(driver, RELATED_ARTICLES)
    assert len(links) > 0
    links[random.randint(1, len(links)) - 1].click()


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)
