# -*- coding: utf-8 -*-
"""Find a Supplier Landing Page Object."""
import logging
import random
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    check_for_sections,
    check_url,
    find_and_click_on_page_element,
    find_element,
    find_elements,
    go_to_url,
    take_screenshot,
)
from pages.fas.header_footer import HEADER_FOOTER_SELECTORS
from settings import DIRECTORY_UI_SUPPLIER_URL

NAME = "Home"
SERVICE = "Find a Supplier"
TYPE = "home"
URL = DIRECTORY_UI_SUPPLIER_URL
PAGE_TITLE = "Find UK suppliers - trade.great.gov.uk"

SEARCH_INPUT = Selector(By.ID, "id_term")
SEARCH_SECTOR = Selector(By.ID, "id_sectors")
SEARCH_BUTTON = Selector(By.CSS_SELECTOR, "#search-area > form button")
CONTACT_US_BUTTON = Selector(By.CSS_SELECTOR, "#introduction-section a")
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
        "first industry": Selector(
            By.CSS_SELECTOR, "#industries-section a:nth-child(1)"
        ),
        "second industry": Selector(
            By.CSS_SELECTOR, "#industries-section a:nth-child(2)"
        ),
        "third industry": Selector(
            By.CSS_SELECTOR, "#industries-section a:nth-child(3)"
        ),
        "see more industries": Selector(
            By.CSS_SELECTOR, "#industries-section > div > a.button"
        ),
    },
    "uk services": {
        "itself": Selector(By.ID, "services-section"),
        "first service": Selector(
            By.CSS_SELECTOR, "#services-section div.column-one-quarter:nth-child(3)"
        ),
        "second service": Selector(
            By.CSS_SELECTOR, "#services-section div.column-one-quarter:nth-child(4)"
        ),
        "third service": Selector(
            By.CSS_SELECTOR, "#services-section div.column-one-quarter:nth-child(5)"
        ),
        "fourth service": Selector(
            By.CSS_SELECTOR, "#services-section div.column-one-quarter:nth-child(6)"
        ),
    },
}
SELECTORS.update(HEADER_FOOTER_SELECTORS)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
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


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)


def open_industry(driver: WebDriver, industry_name: str):
    industry_name = industry_name.split(" - ")[1].strip()
    selector = Selector(By.PARTIAL_LINK_TEXT, industry_name)
    logging.debug("Looking for: {}".format(industry_name))
    industry_link = find_element(
        driver, selector, element_name="Industry card", wait_for_it=False
    )
    industry_link.click()
    take_screenshot(driver, NAME + " after opening " + industry_name + " page")


def see_more_industries(driver: WebDriver):
    click_on_page_element(driver, "see more industries")


def open_any_article(driver: WebDriver):
    selector = Selector(By.CSS_SELECTOR, "#industries-section a.industry-card")
    links = find_elements(driver, selector)
    random.choice(links).click()
