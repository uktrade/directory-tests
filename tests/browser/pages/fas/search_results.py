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
    tick_captcha_checkbox,
    tick_checkboxes,
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
        "q": Selector(By.ID, "id_q", type=ElementType.INPUT),
        "industries": Selector(
            By.CSS_SELECTOR,
            "#checkbox-industry-expertise li input",
            type=ElementType.CHECKBOX,
            is_visible=False,
            alternative_visibility_check=True,
        ),
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
        "t&c": Selector(
            By.ID,
            "id_terms",
            type=ElementType.CHECKBOX,
            is_visible=False,
            alternative_visibility_check=True,
        ),
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
        f"Expected to see {number_expected_filters} sector filter(s) to be checked but "
        f"saw {number_checked_filters}"
    ):
        assert number_checked_filters == number_expected_filters

    diff = list(set(formatted_expected_filters) - set(checked_sector_filters))
    with assertion_msg(
        f"Couldn't find '{diff}' among checked filters: {checked_sector_filters}"
    ):
        assert not diff


def generate_form_details(
    actor: Actor, *, custom_details: dict = None, form_name: str = None
) -> dict:
    if form_name == "subscribe for email updates":
        result = {
            "full name": actor.alias,
            "email": actor.email,
            "industry": None,
            "company name": "AUTOMATED TESTS",
            "country": None,
            "t&c": True,
        }
    elif form_name == "search form":
        result = {
            "q": custom_details["q"] if "q" in custom_details else "food",
            "industries": None,
        }
    else:
        raise KeyError(f"Unexpected form name: {form_name}")
    if custom_details:
        result.update(custom_details)
    if "industries" in result:
        result["industries"] = result["industries"].upper().replace(" ", "_")
    return result


def fill_out(driver: WebDriver, form_details: dict, form_name: str = None):
    if form_name == "subscribe for email updates":
        form_selectors = SELECTORS[form_name]
        fill_out_input_fields(driver, form_selectors, form_details)
        pick_option(driver, form_selectors, form_details)
        tick_checkboxes(driver, form_selectors, form_details)
        tick_captcha_checkbox(driver)
    elif form_name == "search form":
        form_selectors = SELECTORS[form_name]
        fill_out_input_fields(driver, form_selectors, form_details)
        tick_checkboxes(driver, form_selectors, form_details)
    else:
        raise KeyError(f"Unexpected form name: {form_name}")


def submit(driver: WebDriver, form_name: str = None) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS[form_name or "subscribe for email updates"])


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
