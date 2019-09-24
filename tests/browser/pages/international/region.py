# -*- coding: utf-8 -*-
"""Regional page."""
import logging
from typing import List
from urllib.parse import urljoin

from directory_tests_shared.enums import Service
from directory_tests_shared.settings import INTERNATIONAL_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import common_selectors
from pages.common_actions import (
    Selector,
    assertion_msg,
    check_for_sections,
    check_url,
    find_and_click_on_page_element,
    take_screenshot,
    visit_url,
)

NAME = "Region"
NAMES = [
    "London",
    "North England",
    "Northern Ireland",
    "Scotland",
    "South England",
    "Midlands",
    "Wales",
]
SERVICE = Service.INTERNATIONAL
TYPE = "region"
URL = urljoin(INTERNATIONAL_URL, "content/about-uk/regions/")
URL_LEGACY = urljoin(INTERNATIONAL_URL, "content/invest/uk-regions/")
PAGE_TITLE = "Invest in Great Britain - "


SubURLs = {
    "london": urljoin(URL, "london/"),
    "north england": urljoin(URL, "north-england/"),
    "northern ireland": urljoin(URL, "northern-ireland/"),
    "scotland": urljoin(URL_LEGACY, "scotland//"),
    "south england": urljoin(URL, "south-england/"),
    "midlands": urljoin(URL, "midlands/"),
    "wales": urljoin(URL, "wales/"),
}


SELECTORS = {
    "regional breadcrumbs": {
        "great.gov.uk international": Selector(
            By.CSS_SELECTOR, "nav.breadcrumbs ol > li:nth-child(1) > a"),
        "about the uk": Selector(
            By.CSS_SELECTOR, "nav.breadcrumbs ol > li:nth-child(2) > a"),
        "regions": Selector(
            By.CSS_SELECTOR, "nav.breadcrumbs ol > li:nth-child(3) > a"),
    },
}
SELECTORS.update(common_selectors.INTERNATIONAL_HEADER_WO_LANGUAGE_SELECTOR)
SELECTORS.update(common_selectors.INTERNATIONAL_HERO)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.INTERNATIONAL_FOOTER)


def visit(driver: WebDriver, *, page_name: str = None):
    url = SubURLs[page_name] if page_name else URL
    visit_url(driver, url)


def should_be_here(driver: WebDriver, *, page_name: str):
    take_screenshot(driver, PAGE_TITLE)
    url = SubURLs[page_name.lower()] if page_name else URL
    check_url(driver, url)
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


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, PAGE_TITLE + " after clicking on " + element_name)
