# -*- coding: utf-8 -*-
"""Find a Supplier Search Results Page Object."""
import logging
import random
from types import ModuleType
from typing import List, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType, common_selectors
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
    submit_form,
    take_screenshot,
)
from pages.fas import thank_you_for_registering

NAME = "Search results"
SERVICE = Service.FAS
TYPE = PageType.SEARCH_RESULTS
URL = URLs.FAS_SEARCH.absolute
PAGE_TITLE = "Search the database of UK suppliers' trade profiles - trade.great.gov.uk"

SECTOR_FILTERS = Selector(
    By.CSS_SELECTOR, "#checkbox-industry-expertise li input[type=checkbox]"
)
PROFILE_LINKS = Selector(
    By.CSS_SELECTOR, "#companies-column li > a:not(.button-ghost-blue):not(.button)"
)
FILTER_TOGGLE = Selector(By.ID, "toggle_id_industries")
SELECTORS = {
    "search form": {
        "itself": Selector(By.CSS_SELECTOR, "#content form"),
        "search box label": Selector(By.CSS_SELECTOR, "label[for=id_q]"),
        "search box": Selector(By.ID, "id_q"),
        "update results button": Selector(
            By.CSS_SELECTOR,
            "#filter-column button[type=submit]",
            type=ElementType.SUBMIT,
        ),
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
        "number of results": Selector(By.CSS_SELECTOR, "#hero-container h2"),
    },
    "subscribe for email updates": {
        "itself": Selector(
            By.CSS_SELECTOR, "section div.subscription-form-container form"
        ),
        "full name": Selector(By.ID, "id_full_name", type=ElementType.INPUT),
        "email": Selector(By.ID, "id_email_address", type=ElementType.INPUT),
        "industry": Selector(By.ID, "id_sector", type=ElementType.SELECT),
        "company name": Selector(By.ID, "id_company_name", type=ElementType.INPUT),
        "country": Selector(By.ID, "id_country", type=ElementType.SELECT),
        "t&c": Selector(By.ID, "id_terms", type=ElementType.CHECKBOX),
        "captcha": Selector(By.ID, "id_captcha"),
        "send": Selector(
            By.CSS_SELECTOR,
            "#id_terms-container ~ button",
            type=ElementType.SUBMIT,
            next_page=thank_you_for_registering,
        ),
    },
}
SELECTORS.update(common_selectors.INTERNATIONAL_HEADER_WO_LANGUAGE_SELECTOR)
SELECTORS.update(common_selectors.INTERNATIONAL_FOOTER)


def should_be_here(driver: WebDriver):
    show_filters(driver)
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def show_filters(driver: WebDriver):
    filter_toggle = find_element(driver, FILTER_TOGGLE, wait_for_it=False)
    if "checked" in filter_toggle.get_attribute("class"):
        logging.debug(f"Toggling Industry filters")
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


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["search form"])


def open_profile(driver: WebDriver, number: int):
    profile_links = find_elements(driver, PROFILE_LINKS)
    if number == 0:
        link = random.choice(profile_links)
    elif number == 1:
        link = profile_links[0]
    else:
        link = profile_links[0]
    logging.debug(f"Will click on profile link: {link.text}")
    link.click()

    take_screenshot(driver, NAME + " after clicking on company profile link")
