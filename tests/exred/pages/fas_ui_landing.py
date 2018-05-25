# -*- coding: utf-8 -*-
"""Find a Supplier Landing Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import (
    check_for_expected_sections_elements,
    check_for_section,
    check_title,
    check_url,
    go_to_url,
    find_and_click_on_page_element
)
from settings import DIRECTORY_UI_SUPPLIER_URL
from utils import take_screenshot, find_element

NAME = "Find a Supplier Home page"
URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "")
PAGE_TITLE = \
    "Find trade profiles of reliable UK suppliers - trade.great.gov.uk"

SEARCH_INPUT = "#id_term"
SEARCH_SECTOR = "#id_sectors"
SEARCH_BUTTON = "#search-area > form button"
CONTACT_US_BUTTON = "#introduction-section a"
SECTIONS = {
    "hero": {
        "itself": "section#hero",
    },
    "find uk suppliers": {
        "itself": "#search-area",
        "search term input": SEARCH_INPUT,
        "search selectors dropdown": SEARCH_SECTOR,
        "find suppliers button": SEARCH_BUTTON
    },
    "contact us": {
        "itself": "#introduction-section",
        "introduction text": "#introduction-section p",
        "contact us": CONTACT_US_BUTTON
    },
    "uk industries": {
        "itself": "#industries-section",
        "first industry": "#industries-section a:nth-child(1)",
        "second industry": "#industries-section a:nth-child(2)",
        "third industry": "#industries-section a:nth-child(3)",
        "see more button": "#industries-section > div > a.button"
    },
    "uk services": {
        "itself": "#services-section",
        "first service": "#services-section div.column-one-quarter:nth-child(3)",
        "second service": "#services-section div.column-one-quarter:nth-child(4)",
        "third service": "#services-section div.column-one-quarter:nth-child(5)",
        "fourth service": "#services-section div.column-one-quarter:nth-child(6)",
    }
}


def visit(driver: webdriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    check_title(driver, PAGE_TITLE, exact_match=True)
    check_for_expected_sections_elements(driver, SECTIONS)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_section(driver: webdriver, name: str):
    check_for_section(driver, SECTIONS, sought_section=name)


def search(driver: webdriver, *, keyword: str = None, sector: str = None):
    input_field = find_element(
        driver, by_css=SEARCH_INPUT, element_name="Search input field",
        wait_for_it=False)
    input_field.clear()
    if keyword:
        input_field.send_keys(keyword)
    if sector:
        sector_dropdown = find_element(
            driver, by_css=SEARCH_SECTOR, element_name="Sector dropdown menu",
            wait_for_it=False)
        sector_value = "option[value='{}']".format(sector.upper().replace(" ", "_"))
        sector_option = sector_dropdown.find_element_by_css_selector(sector_value)
        sector_option.click()
    take_screenshot(driver, NAME + " after entering the keyword")
    button = find_element(
        driver, by_css=SEARCH_BUTTON, element_name="Search button",
        wait_for_it=False)
    button.click()
    take_screenshot(driver, NAME + " after submitting the search form")


def click_on_page_element(driver: webdriver, element_name: str):
    find_and_click_on_page_element(driver, SECTIONS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)


def open_industry(driver: webdriver, industry_name: str):
    industry_link = find_element(
        driver, by_partial_link_text=industry_name,
        element_name="Industry card", wait_for_it=False)
    industry_link.click()
    take_screenshot(driver, NAME + " after opening " + industry_name + " page")
