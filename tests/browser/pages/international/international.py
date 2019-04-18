# -*- coding: utf-8 -*-
"""International - Landing page"""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import common_selectors
from pages.common_actions import (
    Selector,
    check_for_section,
    check_for_sections,
    check_if_element_is_visible,
    check_url,
    find_and_click_on_page_element,
    find_element,
    go_to_url,
    take_screenshot,
    wait_for_page_load_after_action,
)
from settings import EXRED_UI_URL

NAME = "Landing"
SERVICE = "International"
TYPE = "home"
URL = urljoin(EXRED_UI_URL, "international/")
PAGE_TITLE = "Welcome to great.gov.uk - buy from or invest in the UK"


COUNTRY_SELECTOR = Selector(By.ID, "country-selector-activator")
LANGUAGE_SELECTOR_CLOSE = Selector(By.ID, "header-language-selector-close")
FIND_A_SUPPLIER = Selector(By.ID, "card-fas-link")
SEE_THE_POTENTIAL = Selector(By.ID, "card-invest-link")
LEARN_MORE = Selector(By.ID, "card-study-uk-link")
PLAN_YOUR_TRIP = Selector(By.ID, "card-visit-uk-link")
BETA_FEEDBACK = Selector(By.CSS_SELECTOR, "#header-beta-bar span > a")
SELECTORS = {
    "service cards": {
        "itself": Selector(By.CSS_SELECTOR, "div.card-grid"),
        "cards": Selector(By.CSS_SELECTOR, "#content div.card"),
        "expand to the uk": Selector(By.CSS_SELECTOR, "#content > section > div > div > div:nth-child(1) a"),
        "find a uk supplier": Selector(By.CSS_SELECTOR, "#content > section > div > div > div:nth-child(2) a"),
    },
    "tariffs": {"itself": Selector(By.ID, "tariffs-section")},
    "news": {
        "itself": Selector(By.ID, "news-events-section"),
        "cards": Selector(By.CSS_SELECTOR, "#news-events-section .card"),
    },
    "study or visit the uk": {
        "itself": Selector(By.ID, "study-visit-cta-section"),
        "study in the uk": Selector(By.LINK_TEXT, "Study in the UK"),
        "visit the uk": Selector(By.LINK_TEXT, "Visit the UK"),
    },
}
SELECTORS.update(common_selectors.HEADER_INTERNATIONAL)
SELECTORS.update(common_selectors.BETA_BAR)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.FOOTER_INTERNATIONAL)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)


def should_see_section(driver: WebDriver, name: str):
    check_for_section(driver, SELECTORS, sought_section=name)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


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
