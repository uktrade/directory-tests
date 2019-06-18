# -*- coding: utf-8 -*-
"""Find a Supplier Search Results Page Object."""
import logging
import random
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Actor,
    Selector,
    assertion_msg,
    check_for_sections,
    check_url,
    fill_out_input_fields,
    find_element,
    find_elements,
    pick_option,
    take_screenshot,
)
from pages.fas.header_footer import HEADER_FOOTER_SELECTORS
from settings import DIRECTORY_UI_SUPPLIER_URL

NAME = "Search results"
SERVICE = "Find a Supplier"
TYPE = "search"
URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "search/")
PAGE_TITLE = "Search the database of UK suppliers' trade profiles - trade.great.gov.uk"

SECTOR_FILTERS = Selector(
    By.CSS_SELECTOR, "#checkbox-industry-expertise li input[type=checkbox]"
)
PROFILE_LINKS = Selector(
    By.CSS_SELECTOR, "#companies-column li > a"
)
UPDATE_RESULTS = Selector(By.CSS_SELECTOR, "#filter-column button[type=submit]")
FILTER_TOGGLE = Selector(By.ID, "toggle_id_sectors")
SELECTORS = {
    "search form": {
        "itself": Selector(By.CSS_SELECTOR, "#content form"),
        "search box label": Selector(By.CSS_SELECTOR, "label[for=id_q]"),
        "search box": Selector(By.ID, "id_q"),
        "update results button": UPDATE_RESULTS,
    },
    "filters": {
        "itself": Selector(By.ID, "filter-column"),
        "title": Selector(By.CSS_SELECTOR, "#filter-column section span"),
        "filter list labels": Selector(
            By.CSS_SELECTOR, "#checkbox-industry-expertise li label"
        ),
    },
    "results": {
        "itself": Selector(By.ID, "companies-column"),
        "number of results": Selector(
            By.CSS_SELECTOR, "#hero-container h2"
        ),
    },
}
SELECTORS.update(HEADER_FOOTER_SELECTORS)


def should_be_here(driver: WebDriver):
    show_filters(driver)
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def show_filters(driver: WebDriver):
    filter_toggle = find_element(driver, FILTER_TOGGLE, wait_for_it=False)
    css_classes = filter_toggle.get_attribute("class")
    if "checked" in css_classes:
        filter_toggle.click()


def should_see_filtered_results(driver: WebDriver, expected_filters: List[str]):
    def to_filter_format(name):
        return name.upper().replace(" ", "_").replace("-", "_")

    formatted_expected_filters = list(map(to_filter_format, expected_filters))

    show_filters(driver)
    sector_filters = find_elements(driver, SECTOR_FILTERS)
    checked_sector_filters = [
        sector_filter.get_attribute("value")
        for sector_filter in sector_filters
        if sector_filter.get_attribute("checked")
    ]

    number_expected_filters = len(formatted_expected_filters)
    number_checked_filters = len(checked_sector_filters)
    with assertion_msg(
        "Expected to see %d sector filter(s) to be checked but saw %d",
        number_expected_filters,
        number_checked_filters,
    ):
        assert number_checked_filters == number_expected_filters

    diff = list(set(formatted_expected_filters) - set(checked_sector_filters))
    with assertion_msg("Couldn't find '%s' among checked filters", diff):
        assert not diff


def generate_form_details(actor: Actor, *, custom_details: dict = None) -> dict:
    result = {
        "q": custom_details["q"] if "q" in custom_details else "food",
        "sector": None,
    }
    return result


def fill_out(driver: WebDriver, contact_us_details: dict):
    form_selectors = SELECTORS["search form"]
    fill_out_input_fields(driver, form_selectors, contact_us_details)
    pick_option(driver, form_selectors, contact_us_details)
    take_screenshot(driver, "After filling out the search form")


def submit(driver: WebDriver):
    take_screenshot(driver, "Before submitting the search form")
    button = find_element(
        driver,
        UPDATE_RESULTS,
        element_name="Update results",
        wait_for_it=False,
    )
    button.click()
    take_screenshot(driver, "After submitting the search form")


def open_profile(driver: WebDriver, number: int):
    profile_links = find_elements(driver, PROFILE_LINKS)
    if number == 0:
        link = random.choice(profile_links)
    elif number == 1:
        link = profile_links[0]
    else:
        link = profile_links[0]
    link.click()

    take_screenshot(driver, NAME + " after clicking on company profile link")
