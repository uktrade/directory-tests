# -*- coding: utf-8 -*-
"""ExRed Search Result Page object"""

import logging
import random
import time
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Selector,
    assertion_msg,
    check_url,
    fill_out_input_fields,
    find_and_click_on_page_element,
    find_element,
    find_elements,
    scroll_to,
    take_screenshot,
)
from settings import EXRED_UI_URL

NAME = "Search results"
SERVICE = "Export Readiness"
TYPE = "Search"
URL = urljoin(EXRED_UI_URL, "/search/?q=")

PAGES = Selector(By.CSS_SELECTOR, "ul.navigation li")
PAGINATION = Selector(By.CSS_SELECTOR, "div.pagination")
ACTIVE_PAGE = Selector(By.CSS_SELECTOR, ".pagination ul li span.active")
NEXT = Selector(By.CSS_SELECTOR, ".pagination a.next")
PREVIOUS = Selector(By.CSS_SELECTOR, ".pagination a.previous")
SUBMIT_BUTTON = Selector(
    By.CSS_SELECTOR,
    "#search-box ~ button[type=submit]",
    type=ElementType.BUTTON,
)
SEARCH_RESULTS = Selector(By.CSS_SELECTOR, "ul.results li")
SELECTORS = {
    "form": {
        "search box": Selector(By.ID, "search-box", type=ElementType.INPUT),
        "submit": SUBMIT_BUTTON,
    },
    "results": {
        "itself": Selector(By.ID, "search-results-list"),
        "active_page": ACTIVE_PAGE,
        "pagination": PAGINATION,
        "pages": PAGES,
        "search results": SEARCH_RESULTS,
        "next": NEXT,
        "previous": PREVIOUS,
    },
}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_page_number(driver: WebDriver, page_num: int):
    scroll_to(driver, find_element(driver, ACTIVE_PAGE))
    take_screenshot(driver, NAME)
    selector = find_element(driver, ACTIVE_PAGE)

    with assertion_msg(
        f"Expected to see {page_num} but got {int(selector.text)}"
    ):
        assert int(selector.text) == page_num


def click_on_result_of_type(driver: WebDriver, type_of: str):
    results = find_elements(driver, SEARCH_RESULTS)
    results_of_matching_type = [
        result
        for result in results
        if result.find_element_by_css_selector("span.type").text.lower()
        == type_of.lower()
    ]

    with assertion_msg(
        f"Expected to see at least 1 search result of type '{type_of}' but found none"
    ):
        assert results_of_matching_type
    logging.debug(
        f"Found {len(results_of_matching_type)} results of type '{type_of}'"
    )
    result = random.choice(results_of_matching_type)
    result_link = result.find_element_by_css_selector("a")
    logging.debug(
        f"Will click on {result_link.text} -> {result_link.get_property('href')}"
    )
    result_link.click()


def has_pagination(driver: WebDriver, min_page_num: int):
    scroll_to(driver, find_element(driver, PAGINATION))
    take_screenshot(driver, NAME)
    time.sleep(2)
    selectors = find_elements(driver, PAGES)
    with assertion_msg(
        f"Expected to see more that {min_page_num} search results page but got just {len(selectors)}"
    ):
        assert len(selectors) > min_page_num


def click_on_page_element(driver, element_name):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)


def paginator(driver: WebDriver, existing_page: str):
    selector = find_element(driver, NEXT)
    existing_page_text = selector.text
    with assertion_msg(
        f"Expected to see {existing_page} page but got {existing_page_text}"
    ):
        assert existing_page == existing_page_text


def search(driver: WebDriver, phrase: str):
    form_selectors = SELECTORS["form"]
    search_phrase = {"search box": phrase}
    button = find_element(driver, SUBMIT_BUTTON, wait_for_it=True)
    fill_out_input_fields(driver, form_selectors, search_phrase)
    button.click()
    take_screenshot(driver, "After submitting the form")
