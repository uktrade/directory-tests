# -*- coding: utf-8 -*-
"""Find a Supplier Landing Page Object."""
import logging
from typing import List
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.common.by import By

from pages.common_actions import (
    AssertionExecutor,
    Selector,
    check_for_expected_sections_elements,
    check_for_sections,
    check_title,
    check_url,
    find_and_click_on_page_element,
    find_element,
    go_to_url,
    take_screenshot,
)
from settings import DIRECTORY_UI_SUPPLIER_URL

NAME = "Home"
SERVICE = "Find a Supplier"
TYPE = "home"
URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "/")
PAGE_TITLE = "Find UK suppliers - trade.great.gov.uk"

SEARCH_INPUT = "id_term"
SEARCH_SECTOR = "id_sectors"
SEARCH_BUTTON = "#search-area > form button"
CONTACT_US_BUTTON = "#introduction-section a"
SELECTORS = {
    "hero": {"itself": Selector(By.CSS_SELECTOR, "section#hero")},
    "find uk suppliers": {
        "itself": Selector(By.ID, "search-area"),
        "search term input": Selector(By.ID, SEARCH_INPUT),
        "search selectors dropdown": Selector(By.ID, SEARCH_SECTOR),
        "find suppliers button": Selector(By.CSS_SELECTOR, SEARCH_BUTTON),
    },
    "contact us": {
        "itself": Selector(By.ID, "introduction-section"),
        "introduction text": Selector(By.CSS_SELECTOR, "#introduction-section p"),
        "contact us": Selector(By.CSS_SELECTOR, CONTACT_US_BUTTON),
    },
    "uk industries": {
        "itself": Selector(By.ID, "industries-section"),
        "first industry": Selector(By.CSS_SELECTOR, "#industries-section a:nth-child(1)"),
        "second industry": Selector(By.CSS_SELECTOR, "#industries-section a:nth-child(2)"),
        "third industry": Selector(By.CSS_SELECTOR, "#industries-section a:nth-child(3)"),
        "see more industries": Selector(By.CSS_SELECTOR, "#industries-section > div > a.button"),
    },
    "uk services": {
        "itself": Selector(By.ID, "services-section"),
        "first service": Selector(By.CSS_SELECTOR, "#services-section div.column-one-quarter:nth-child(3)"),
        "second service": Selector(By.CSS_SELECTOR, "#services-section div.column-one-quarter:nth-child(4)"),
        "third service": Selector(By.CSS_SELECTOR, "#services-section div.column-one-quarter:nth-child(5)"),
        "fourth service": Selector(By.CSS_SELECTOR, "#services-section div.column-one-quarter:nth-child(6)"),
    },
}


def visit(driver: webdriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    check_title(driver, PAGE_TITLE, exact_match=True)
    check_for_expected_sections_elements(driver, SELECTORS)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(executor: AssertionExecutor, names: List[str]):
    check_for_sections(executor, all_sections=SELECTORS, sought_sections=names)


def search(driver: webdriver, *, keyword: str = None, sector: str = None):
    input_field = find_element(
        driver,
        by_css=SEARCH_INPUT,
        element_name="Search input field",
        wait_for_it=False,
    )
    input_field.clear()
    if keyword:
        input_field.send_keys(keyword)
    if sector:
        sector_dropdown = find_element(
            driver,
            by_css=SEARCH_SECTOR,
            element_name="Sector dropdown menu",
            wait_for_it=False,
        )
        sector_value = "option[value='{}']".format(sector.upper().replace(" ", "_"))
        sector_option = sector_dropdown.find_element_by_css_selector(sector_value)
        sector_option.click()
    take_screenshot(driver, NAME + " after entering the keyword")
    button = find_element(
        driver, by_css=SEARCH_BUTTON, element_name="Search button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, NAME + " after submitting the search form")


def click_on_page_element(driver: webdriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)


def clean_name(name: str) -> str:
    return name.replace("Find a Supplier - ", "").replace("industry", "").strip()


def open_industry(driver: webdriver, industry_name: str):
    industry_name = clean_name(industry_name)
    logging.debug("Looking for: {}".format(industry_name))
    industry_link = find_element(
        driver,
        by_partial_link_text=industry_name,
        element_name="Industry card",
        wait_for_it=False,
    )
    industry_link.click()
    take_screenshot(driver, NAME + " after opening " + industry_name + " page")


def see_more_industries(driver: webdriver):
    click_on_page_element(driver, "see more industries")
