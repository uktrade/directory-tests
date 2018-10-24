# -*- coding: utf-8 -*-
"""great.gov.uk International page"""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    check_for_expected_sections_elements,
    check_for_section,
    check_if_element_is_visible,
    check_url,
    find_element,
    go_to_url,
    take_screenshot,
    wait_for_page_load_after_action,
    check_for_sections,
    AssertionExecutor,
    find_and_click_on_page_element
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
FIND_A_SUPPLIER = Selector(By.ID, "card-fas-link")
SEE_THE_POTENTIAL = Selector(By.ID, "card-invest-link")
LEARN_MORE = Selector(By.ID, "card-study-uk-link")
PLAN_YOUR_TRIP = Selector(By.ID, "card-visit-uk-link")
BETA_FEEDBACK = Selector(By.CSS_SELECTOR, "#header-beta-bar span > a")
SELECTORS = {
    "header bar": {
        "itself": Selector(By.ID, "international-header-bar"),
        "language selector": LANGUAGE_SELECTOR,
    },
    "beta bar": {
        "itself": Selector(By.ID, "header-beta-bar"),
        "badge": Selector(By.CSS_SELECTOR, "#header-beta-bar .phase-tag"),
        "message": Selector(By.CSS_SELECTOR, "#header-beta-bar span"),
        "link": Selector(By.CSS_SELECTOR, "#header-beta-bar a"),
    },
    "header menu": {
        "itself": Selector(By.ID, "international-header-menu"),
        "logo": Selector(By.ID, "international-header-logo"),
    },
    "eu exit updates": {
        "itself": Selector(By.ID, "eu-exit-banner"),
        "badge": Selector(By.CSS_SELECTOR, "#eu-exit-banner div.banner-badge"),
        "see our updates on eu exit": Selector(
            By.CSS_SELECTOR, "#eu-exit-banner a"),
    },
    "intro": {
        "itself": Selector(By.CSS_SELECTOR, "#content > section.intro"),
        "title": Selector(By.CSS_SELECTOR, "#content > section.intro h1"),
        "description": Selector(By.CSS_SELECTOR, "#content > section.intro p"),
    },
    "buy from the uk": {
        "itself": Selector(By.ID, "card-fas"),
        "image": Selector(By.ID, "card-fas-image"),
        "title": Selector(By.CSS_SELECTOR, "#card-fas h3"),
        "text": Selector(By.CSS_SELECTOR, "#card-fas p"),
        "find a supplier - home": FIND_A_SUPPLIER,
    },
    "invest in the uk": {
        "itself": Selector(By.ID, "card-invest"),
        "image": Selector(By.ID, "card-invest-image"),
        "title": Selector(By.CSS_SELECTOR, "#card-invest h3"),
        "text": Selector(By.CSS_SELECTOR, "#card-invest p"),
        "invest - home": SEE_THE_POTENTIAL,
    },
    "study in the uk": {
        "itself": Selector(By.ID, "card-study-uk"),
        "image": Selector(By.ID, "card-study-uk-image"),
        "title": Selector(By.CSS_SELECTOR, "#card-study-uk h3"),
        "text": Selector(By.CSS_SELECTOR, "#card-study-uk p"),
        "british council - home": LEARN_MORE,
    },
    "visit the uk": {
        "itself": Selector(By.ID, "card-visit-uk"),
        "image": Selector(By.ID, "card-visit-uk-image"),
        "title": Selector(By.CSS_SELECTOR, "#card-visit-uk h3"),
        "text": Selector(By.CSS_SELECTOR, "#card-visit-uk p"),
        "visit britain - home": PLAN_YOUR_TRIP,
    },
}


def visit(driver: WebDriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
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


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)
