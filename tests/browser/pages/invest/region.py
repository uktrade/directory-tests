# -*- coding: utf-8 -*-
"""Invest in Great Regional Page Object."""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    assertion_msg,
    check_for_sections,
    check_url,
    find_and_click_on_page_element,
    find_elements,
    take_screenshot,
    visit_url,
)
from settings import INVEST_UI_URL

NAME = "Region"
NAMES = [
    "London",
    "North England",
    "Northern Ireland",
    "Scotland",
    "South of England",
    "The Midlands",
    "Wales",
]
SERVICE = "invest"
TYPE = "region"
URL = urljoin(INVEST_UI_URL, "uk-regions/")
BASE_URL = urljoin(INVEST_UI_URL, "uk-regions/")
PAGE_TITLE = "Invest in Great Britain - "


URLs = {
    "london": urljoin(BASE_URL, "london/"),
    "north england": urljoin(BASE_URL, "north-england/"),
    "northern ireland": urljoin(BASE_URL, "northern-ireland/"),
    "scotland": urljoin(BASE_URL, "scotland/"),
    "south of england": urljoin(BASE_URL, "south-england/"),
    "the midlands": urljoin(BASE_URL, "midlands/"),
    "wales": urljoin(BASE_URL, "wales/"),
}


TOPIC_EXPANDERS = Selector(
    By.CSS_SELECTOR, "section.setup-guide a.accordion-expander"
)

SELECTORS = {
    "header": {
        "self": Selector(By.ID, "invest-header"),
        "logo": Selector(
            By.CSS_SELECTOR, "#invest-header > div.header-bar  a"
        ),
        "contact us": Selector(
            By.CSS_SELECTOR, "#invest-header a[href='/contact/']"
        ),
    },
    "beta bar": {
        "self": Selector(By.ID, "header-beta-bar"),
        "beta bar": Selector(By.CSS_SELECTOR, "#header-beta-bar strong"),
        "feedback": Selector(By.CSS_SELECTOR, "#header-beta-bar a"),
    },
    "hero": {"self": Selector(By.CSS_SELECTOR, "#content > section.hero")},
    "topics": {
        "self": Selector(By.CSS_SELECTOR, "#content > section.setup-guide > div > ul"),
        "accordion expanders": TOPIC_EXPANDERS,
    },
    "topics contents": {
        "paragraphs": Selector(By.CSS_SELECTOR, "div.accordion-content p")
    },
    "report this page": {
        "self": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "report link": Selector(By.CSS_SELECTOR, "section.error-reporting a"),
    },
    "footer": {
        "self": Selector(By.ID, "invest-footer"),
        "uk gov logo": Selector(
            By.CSS_SELECTOR,
            "#invest-footer div.footer-branding > img:nth-child(1)",
        ),
        "invest logo": Selector(
            By.CSS_SELECTOR,
            "#invest-footer div.footer-branding > img:nth-child(2)",
        ),
    },
}


def visit(driver: WebDriver, *, page_name: str = None):
    key = page_name.split(" - ")[1].lower()
    url = URLs[key]
    visit_url(driver, url)


def should_be_here(driver: WebDriver, *, page_name: str):
    take_screenshot(driver, PAGE_TITLE)
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def open_link(driver: WebDriver, name: str):
    driver.find_element_by_link_text(name).click()


def clean_name(name: str) -> str:
    return name.split(" - ")[1].strip()


def should_see_content_for(driver: WebDriver, region_name: str):
    source = driver.page_source
    region_name = clean_name(region_name)
    logging.debug("Looking for: {}".format(region_name))
    with assertion_msg(
        "Expected to find term '%s' in the source of the page %s",
        region_name,
        driver.current_url,
    ):
        assert region_name.lower() in source.lower()


def unfold_topics(driver: WebDriver):
    expanders = find_elements(driver, TOPIC_EXPANDERS)
    assert (
        expanders
    ), "Expected to see at least 1 topic but found 0 on {}".format(
        driver.current_url
    )
    for expander in expanders:
        expander.click()


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, PAGE_TITLE + " after clicking on " + element_name)
