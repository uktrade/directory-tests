# -*- coding: utf-8 -*-
"""great.gov.uk International page"""
import logging
from typing import List
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    check_for_expected_sections_elements,
    check_for_section,
    check_if_element_is_visible,
    check_title,
    check_url,
    find_element,
    go_to_url,
    take_screenshot,
    wait_for_page_load_after_action,
    check_for_sections,
    AssertionExecutor
)
from settings import EXRED_UI_URL

NAME = "International"
SERVICE = "Export Readiness"
TYPE = "home"
URL = urljoin(EXRED_UI_URL, "international/")
PAGE_TITLE = "Welcome to great.gov.uk - buy from or invest in the UK"


LANGUAGE_SELECTOR = Selector(
    By.CSS_SELECTOR, "#international-header-bar .LanguageSelectorDialog-Tracker"
)
LANGUAGE_SELECTOR_CLOSE = Selector(By.ID, "header-language-selector-close")
FIND_A_SUPPLIER = Selector(
    By.CSS_SELECTOR, "section:nth-child(2) div:nth-child(1) > div > div.card-inner > a"
)
SEE_THE_POTENTIAL = Selector(
    By.CSS_SELECTOR, "section:nth-child(2) div:nth-child(2) > div > div.card-inner > a"
)
LEARN_MORE = Selector(
    By.CSS_SELECTOR, "section:nth-child(2) div:nth-child(3) > div > div.card-inner > a"
)
PLAN_YOUR_TRIP = Selector(
    By.CSS_SELECTOR, "section:nth-child(2) div:nth-child(4) > div > div.card-inner > a"
)
BETA_FEEDBACK = Selector(By.CSS_SELECTOR, "#header-beta-bar span > a")
SELECTORS = {
    "header bar": {
        "itself": Selector(By.ID, "international-header-bar"),
        "language selector": LANGUAGE_SELECTOR,
    },
    "header-menu": {
        "itself": Selector(By.ID, "international-header-menu"),
        "logo": Selector(By.ID, "international-header-logo"),
    },
    "intro": {
        "itself": Selector(By.CSS_SELECTOR, "#content > section.intro"),
        "title": Selector(By.CSS_SELECTOR, "#content > section.intro h1"),
        "description": Selector(By.CSS_SELECTOR, "#content > section.intro p"),
    },
    "buy from the uk": {
        "itself": Selector(
            By.CSS_SELECTOR, "section:nth-child(2) div:nth-child(1) > div.card"
        ),
        "image": Selector(
            By.CSS_SELECTOR, "section:nth-child(2) div:nth-child(1) > div > div.card-image"
        ),
        "title": Selector(
            By.CSS_SELECTOR, "section:nth-child(2) div:nth-child(1) > div > div.card-inner > h3"
        ),
        "text": Selector(
            By.CSS_SELECTOR, "section:nth-child(2) div:nth-child(1) > div > div.card-inner > p"
        ),
        "find a supplier - home": FIND_A_SUPPLIER,
    },
    "invest in the uk": {
        "itself": Selector(
            By.CSS_SELECTOR, "section:nth-child(2) div:nth-child(2) > div.card"
        ),
        "image": Selector(
            By.CSS_SELECTOR, "section:nth-child(2) div:nth-child(2) > div > div.card-image"
        ),
        "title": Selector(
            By.CSS_SELECTOR, "section:nth-child(2) div:nth-child(2) > div > div.card-inner > h3"
        ),
        "text": Selector(
            By.CSS_SELECTOR, "section:nth-child(2) div:nth-child(2) > div > div.card-inner > p"
        ),
        "invest - home": SEE_THE_POTENTIAL,
    },
    "study in the uk": {
        "itself": Selector(
            By.CSS_SELECTOR, "section:nth-child(2) div:nth-child(3) > div.card"
        ),
        "image": Selector(
            By.CSS_SELECTOR, "section:nth-child(2) div:nth-child(3) > div > div.card-image"
        ),
        "title": Selector(
            By.CSS_SELECTOR, "section:nth-child(2) div:nth-child(3) > div > div.card-inner > h3"
        ),
        "text": Selector(
            By.CSS_SELECTOR, "section:nth-child(2) div:nth-child(3) > div > div.card-inner > p"
        ),
        "british council - home": LEARN_MORE,
    },
    "visit the uk": {
        "itself": Selector(
            By.CSS_SELECTOR, "section:nth-child(2) div:nth-child(4) > div.card"
        ),
        "image": Selector(
            By.CSS_SELECTOR, "section:nth-child(2) div:nth-child(4) > div > div.card-image"
        ),
        "title": Selector(
            By.CSS_SELECTOR, "section:nth-child(2) div:nth-child(4) > div > div.card-inner > h3"
        ),
        "text": Selector(
            By.CSS_SELECTOR, "section:nth-child(2) div:nth-child(4) > div > div.card-inner > p"
        ),
        "visit britain - home": PLAN_YOUR_TRIP,
    },
}


def visit(driver: WebDriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    check_title(driver, PAGE_TITLE, exact_match=True)
    check_for_expected_sections_elements(driver, SELECTORS)


def should_see_section(driver: WebDriver, name: str):
    check_for_section(driver, SELECTORS, sought_section=name)


def should_see_sections(executor: AssertionExecutor, names: List[str]):
    check_for_sections(executor, all_sections=SELECTORS, sought_sections=names)


def open(driver: WebDriver, group: str, element: str, *, same_tab: bool = True):
    selector = SELECTORS[group.lower()][element.lower()]
    link = find_element(driver, selector, element_name=element, wait_for_it=False)
    check_if_element_is_visible(link, element_name=element)
    if same_tab:
        href = link.get_attribute("href")
        logging.debug("Opening '%s' link '%s' in the same tab", element, href)
        driver.get(href)
    else:
        with wait_for_page_load_after_action(driver):
            link.click()
    take_screenshot(driver, NAME + " after clicking on: %s link".format(element))
