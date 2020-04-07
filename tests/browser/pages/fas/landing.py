# -*- coding: utf-8 -*-
"""Find a Supplier Landing Page Object."""
import logging
import random
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import common_selectors
from pages.common_actions import (
    Selector,
    check_for_sections,
    check_if_element_is_visible,
    check_url,
    find_element,
    find_elements,
    go_to_url,
    take_screenshot,
    wait_for_page_load_after_action,
)

NAME = "Landing"
SERVICE = Service.FAS
TYPE = PageType.LANDING
URL = URLs.FAS_LANDING.absolute
PAGE_TITLE = "Find UK suppliers - trade.great.gov.uk"

SEARCH_INPUT = Selector(By.CSS_SELECTOR, "#search-area form input[name=q]")
SEARCH_SECTOR = Selector(By.ID, "id_industries")
SEARCH_BUTTON = Selector(By.CSS_SELECTOR, "#search-area > form button")
CONTACT_US_BUTTON = Selector(By.CSS_SELECTOR, "#introduction-section a")
INDUSTRY_CARDS = Selector(By.CSS_SELECTOR, "#industries-section a.labelled-image-card")
SELECTORS = {
    "hero": {"itself": Selector(By.CSS_SELECTOR, "section#hero")},
    "find uk suppliers": {
        "itself": Selector(By.ID, "search-area"),
        "search term input": SEARCH_INPUT,
        "search selectors dropdown": SEARCH_SECTOR,
        "find suppliers button": SEARCH_BUTTON,
    },
    "contact us": {
        "itself": Selector(By.ID, "introduction-section"),
        "introduction text": Selector(By.CSS_SELECTOR, "#introduction-section p"),
        "contact us": CONTACT_US_BUTTON,
    },
    "uk industries": {
        "itself": Selector(By.ID, "industries-section"),
        "industry cards": INDUSTRY_CARDS,
        "first industry": Selector(
            By.CSS_SELECTOR, "#industries-section ul li:nth-child(1) > a"
        ),
        "second industry": Selector(
            By.CSS_SELECTOR, "#industries-section ul li:nth-child(2) > a"
        ),
        "third industry": Selector(
            By.CSS_SELECTOR, "#industries-section ul li:nth-child(3) > a"
        ),
        "see more industries": Selector(
            By.CSS_SELECTOR, "#industries-section a.button"
        ),
    },
    "how we can help": {
        "itself": Selector(By.ID, "services-section"),
        "help options": Selector(
            By.CSS_SELECTOR, "#services-section div.column-quarter-xl"
        ),
    },
}
SELECTORS.update(common_selectors.INTERNATIONAL_HEADER)
SELECTORS.update(common_selectors.INTERNATIONAL_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def search(driver: WebDriver, *, keyword: str = None, sector: str = None):
    input_field = find_element(
        driver, SEARCH_INPUT, element_name="Search input field", wait_for_it=False
    )
    input_field.clear()
    if keyword:
        input_field.send_keys(keyword)
    if sector:
        sector_dropdown = find_element(
            driver,
            SEARCH_SECTOR,
            element_name="Sector dropdown menu",
            wait_for_it=False,
        )
        sector_value = "option[value='{}']".format(sector.upper().replace(" ", "_"))
        sector_option = sector_dropdown.find_element_by_css_selector(sector_value)
        sector_option.click()
    take_screenshot(driver, NAME + " after entering the keyword")
    button = find_element(
        driver, SEARCH_BUTTON, element_name="Search button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, NAME + " after submitting the search form")


def open_industry(driver: WebDriver, industry_name: str):
    industry_name = industry_name.split(" - ")[1].strip()
    selector = Selector(By.PARTIAL_LINK_TEXT, industry_name)
    logging.debug("Looking for: {}".format(industry_name))
    industry_link = find_element(
        driver, selector, element_name="Industry card", wait_for_it=False
    )
    industry_link.click()
    take_screenshot(driver, NAME + " after opening " + industry_name + " page")


def open_any_article(driver: WebDriver) -> str:
    links = find_elements(driver, INDUSTRY_CARDS)
    link = random.choice(links)
    link_text = link.text
    check_if_element_is_visible(link, element_name=link_text)
    with wait_for_page_load_after_action(driver):
        link.click()
    return link_text
