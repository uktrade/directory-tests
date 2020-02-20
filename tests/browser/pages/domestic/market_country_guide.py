# -*- coding: utf-8 -*-
"""Domestic - Country Guide page"""
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from directory_tests_shared.utils import check_url_path_matches_template
from pages import ElementType, common_selectors
from pages.common_actions import Selector, check_for_sections, go_to_url
from pages.domestic import actions as domestic_actions

NAME = "Markets"
SERVICE = Service.DOMESTIC
TYPE = PageType.GUIDE
URL = URLs.DOMESTIC_MARKETS_GUIDE.absolute_template

NAMES = [
    "Brazil",
    "China",
    "Denmark",
    "Germany",
    "Ireland",
    "Italy",
    "Japan",
    "Morocco",
    "South Korea",
    "The Netherlands",
    "Turkey",
]
SubURLs = {
    "brazil": URL.format(country="brazil"),
    "china": URL.format(country="china"),
    "denmark": URL.format(country="denmark"),
    "germany": URL.format(country="germany"),
    "ireland": URL.format(country="ireland"),
    "italy": URL.format(country="italy"),
    "japan": URL.format(country="japan"),
    "morocco": URL.format(country="morocco"),
    "south korea": URL.format(country="south-korea"),
    "the netherlands": URL.format(country="netherlands"),
    "turkey": URL.format(country="turkey"),
}
SELECTORS = {
    "description": {
        "intro": Selector(By.ID, "country-guide-teaser-section"),
        "description": Selector(By.ID, "country-guide-section-one"),
        "statistics": Selector(By.ID, "country-guide-statistics-section"),
    },
    "opportunities for exporters": {
        "self": Selector(By.ID, "country-guide-section-two"),
        "accordions": Selector(By.ID, "country-guide-accordions"),
    },
    "doing business in": {"self": Selector(By.ID, "country-guide-section-three")},
    "next steps": {
        "self": Selector(By.ID, "country-guide-need-help-section"),
        "read more advice about doing business abroad": Selector(
            By.CSS_SELECTOR,
            "#country-guide-need-help-section a[href='/advice/']",
            type=ElementType.LINK,
        ),
        "get in touch with one of our trade advisers": Selector(
            By.CSS_SELECTOR,
            "#country-guide-need-help-section a[href$='office-finder/']",
            type=ElementType.LINK,
        ),
        "check duties and customs procedures for exporting goods": Selector(
            By.CSS_SELECTOR,
            "#country-guide-need-help-section a[href*=duties]",
            type=ElementType.LINK,
            is_visible=False,
        ),
    },
}
SELECTORS.update(common_selectors.DOMESTIC_HEADER)
SELECTORS.update(common_selectors.DOMESTIC_HERO_WO_LINK)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.DOMESTIC_FOOTER)


def visit(driver: WebDriver, *, page_name: str = None):
    url = SubURLs[page_name] if page_name else URL
    go_to_url(driver, url, page_name or NAME)


def should_be_here(driver: WebDriver, *, page_name: str = None):
    check_url_path_matches_template(URL, driver.current_url)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def search(driver: WebDriver, phrase: str):
    domestic_actions.search(driver, phrase)
