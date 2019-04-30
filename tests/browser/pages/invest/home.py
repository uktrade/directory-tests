# -*- coding: utf-8 -*-
"""Invest in Great Home Page Object."""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType, common_selectors
from pages.common_actions import (
    Selector,
    assertion_msg,
    check_for_sections,
    check_title,
    find_and_click_on_page_element,
    find_element,
    find_elements,
    take_screenshot,
    visit_url,
)
from settings import INVEST_UI_URL

NAME = "Home"
URL = urljoin(INVEST_UI_URL, "")
SERVICE = "Invest"
TYPE = "home"
PAGE_TITLE = "Invest in Great Britain - Home"

SELECTORS = {
    "hero": {
        "self": Selector(By.CSS_SELECTOR, "#content > section.hero"),
        "heading": Selector(By.CSS_SELECTOR, "#content > section.hero h1"),
        "get in touch": Selector(By.CSS_SELECTOR, "#content > section.hero a", type=ElementType.LINK),
    },
    "benefits": {
        "self": Selector(By.CSS_SELECTOR, "section.landing-page-benefits"),
        "heading": Selector(By.CSS_SELECTOR, "section.landing-page-benefits h2"),
        "sub-section headings": Selector(By.CSS_SELECTOR, "section.landing-page-benefits h4"),
        "text": Selector(By.CSS_SELECTOR, "section.landing-page-benefits p"),
        "image": Selector(By.CSS_SELECTOR, "section.landing-page-benefits img"),

    },
    "the uk and the eu": {
        "self": Selector(By.CSS_SELECTOR, "#content > section:nth-child(5)"),
        "heading": Selector(By.CSS_SELECTOR, "#content > section:nth-child(5) h2"),
        "text": Selector(By.CSS_SELECTOR, "#content > section:nth-child(5) p"),
        "image": Selector(By.CSS_SELECTOR, "#content > section:nth-child(5) img"),
        "find out what's changing": Selector(By.CSS_SELECTOR, "#content > section:nth-child(5) a", type=ElementType.LINK),

    },
    "invest your capital": {
        "self": Selector(By.CSS_SELECTOR, "div.informative-banner"),
        "heading": Selector(By.CSS_SELECTOR, "div.informative-banner h2"),
        "text": Selector(By.CSS_SELECTOR, "div.informative-banner p"),

    },
    "sectors": {
        "self": Selector(By.CSS_SELECTOR, "#content > section:nth-child(7)"),
        "heading": Selector(By.CSS_SELECTOR, "#content > section:nth-child(7) h2"),
        "heading text": Selector(By.CSS_SELECTOR, "#content > section:nth-child(7) h2 ~ div > p"),
        "first": Selector(
            By.CSS_SELECTOR,
            "#content > section:nth-child(7) > div > div.card-grid > div:nth-child(1) > div > a",
        ),
        "second": Selector(
            By.CSS_SELECTOR,
            "#content > section:nth-child(7) > div > div.card-grid > div:nth-child(2) > div > a",
        ),
        "third": Selector(
            By.CSS_SELECTOR,
            "#content > section:nth-child(7) > div > div.card-grid > div:nth-child(3) > div > a",
        ),
        "see more industries": Selector(
            By.CSS_SELECTOR, "#content > section:nth-child(7) > div > a"
        ),
    },
    "high-potential opportunities": {
        "self": Selector(By.CSS_SELECTOR, "#content > section:nth-child(8)"),
        "heading": Selector(By.CSS_SELECTOR, "#content > section:nth-child(8) h2"),
        "text": Selector(By.CSS_SELECTOR, "#content > section:nth-child(8) h2 ~ div > p"),
        "advanced food production": Selector(By.CSS_SELECTOR, "#content > section:nth-child(8) > div > div.card-grid > div:nth-child(1) > div > a"),
        "lightweight structures": Selector(By.CSS_SELECTOR, "#content > section:nth-child(8) > div > div.card-grid > div:nth-child(2) > div > a"),
        "rail infrastructure": Selector(By.CSS_SELECTOR, "#content > section:nth-child(8) > div > div.card-grid > div:nth-child(3) > div > a"),
    },
    "how to setup in the uk": {
        "self": Selector(By.CSS_SELECTOR, "section.landing-page-setup-guide"),
        "heading": Selector(By.CSS_SELECTOR, "section.landing-page-setup-guide h2"),
        "text": Selector(By.CSS_SELECTOR, "section.landing-page-setup-guide p"),
        "image": Selector(By.CSS_SELECTOR, "section.landing-page-setup-guide img"),
        "get started": Selector(By.CSS_SELECTOR, "section.landing-page-setup-guide a", type=ElementType.LINK),
    },
    "investment support directory": {
        "self": Selector(By.CSS_SELECTOR, "#content > section:nth-child(10)"),
        "heading": Selector(By.CSS_SELECTOR, "#content > section:nth-child(10) h2"),
        "text": Selector(By.CSS_SELECTOR, "#content > section:nth-child(10) p"),
        "image": Selector(By.CSS_SELECTOR, "#content > section:nth-child(10) img"),
        "find a uk specialist": Selector(By.CSS_SELECTOR, "#content > section:nth-child(10) a"),

    },
    "how we help": {
        "self": Selector(By.CSS_SELECTOR, "section.landing-page-how-we-help"),
        "build connections - icon": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-how-we-help ul > li:nth-child(1) > div > img",
        ),
        "build connections - text": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-how-we-help ul > li:nth-child(1) > div > p",
        ),
        "apply for visas - icon": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-how-we-help ul > li:nth-child(2) > div > img",
        ),
        "apply for visas - text": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-how-we-help ul > li:nth-child(2) > div > p",
        ),
        "find grants - icon": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-how-we-help ul > li:nth-child(3) > div > img",
        ),
        "find grants - text": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-how-we-help ul > li:nth-child(3) > div > p",
        ),
        "get insights - icon": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-how-we-help ul > li:nth-child(4) > div > img",
        ),
        "get insights - text": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-how-we-help ul > li:nth-child(4) > div > p",
        ),
        "grow workforce - icon": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-how-we-help ul > li:nth-child(5) > div > img",
        ),
        "grow workforce - text": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-how-we-help ul > li:nth-child(5) > div > p",
        ),
    },
    "contact us": {
        "self": Selector(By.CSS_SELECTOR, "#content > section:nth-child(12)"),
        "heading": Selector(By.CSS_SELECTOR, "#content > section:nth-child(12) h2"),
        "text": Selector(By.CSS_SELECTOR, "#content > section:nth-child(12) p"),
        "get in touch": Selector(By.CSS_SELECTOR, "#content > section:nth-child(12) a", type=ElementType.LINK),

    },
}
SELECTORS.update(common_selectors.HEADER_INVEST)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.BETA_BAR)
SELECTORS.update(common_selectors.EU_EXIT_NEWS_BANNER)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.FOOTER_INVEST)


def visit(driver: WebDriver):
    visit_url(driver, URL)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, PAGE_TITLE)
    check_title(driver, PAGE_TITLE, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def open_link(driver: WebDriver, name: str):
    driver.find_element_by_link_text(name).click()


def open_all_topics(driver: WebDriver):
    topic_links = find_elements(driver, TOPIC_LINKS)
    for link in topic_links:
        link.click()


def clean_name(name: str) -> str:
    return name.split(" - ")[1].strip()


def open_industry(driver: WebDriver, industry_name: str):
    industry_name = clean_name(industry_name)
    selector = Selector(By.PARTIAL_LINK_TEXT, industry_name)
    logging.debug("Looking for: {}".format(industry_name))
    industry_link = find_element(
        driver, selector, element_name="Industry card", wait_for_it=False
    )
    industry_link.click()
    take_screenshot(driver, PAGE_TITLE + " after opening " + industry_name)


def open_guide(driver: WebDriver, guide_name: str):
    guide_name = clean_name(guide_name)
    selector = Selector(By.PARTIAL_LINK_TEXT, guide_name)
    logging.debug("Looking for: {}".format(guide_name))
    guide = find_element(driver, selector, element_name="Guide card", wait_for_it=False)
    guide.click()
    take_screenshot(driver, PAGE_TITLE + " after opening " + guide_name)


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, PAGE_TITLE + " after clicking on " + element_name)
