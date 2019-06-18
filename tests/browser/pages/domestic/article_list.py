# -*- coding: utf-8 -*-
"""ExRed Article List Page Object."""
import logging
from typing import List

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    assertion_msg,
    check_for_expected_sections_elements,
    check_for_section,
    check_for_sections,
    check_if_element_is_not_visible,
    find_element,
    take_screenshot,
)

NAME = "Article List"
SERVICE = "Export Readiness"
TYPE = "article list"
URL = None

SHOW_MORE_BUTTON = Selector(By.ID, "js-paginate-list-more")
ARTICLE_CATEGORY = Selector(By.CSS_SELECTOR, "#content > section h1.title")
BREADCRUMBS = Selector(By.CSS_SELECTOR, "div.breadcrumbs")
ARTICLE_CATEGORY_INTRO = Selector(By.CSS_SELECTOR, "div.section-intro")
LIST_OF_ARTICLES = Selector(By.ID, "js-paginate-list")
TOTAL_NUMBER_OF_ARTICLES = Selector(By.CSS_SELECTOR, "dd.position > span.to")
ARTICLES_TO_READ_COUNTER = Selector(By.CSS_SELECTOR, "dd.position > span.from")
TIME_TO_COMPLETE = Selector(By.CSS_SELECTOR, "dd.time span.value")
IS_THERE_ANYTHING_WRONG_WITH_THIS_PAGE_LINK = Selector(
    By.CSS_SELECTOR, "section.error-reporting a"
)
REGISTER = Selector(
    By.CSS_SELECTOR, "#articles > div > div.scope-indicator > p > a:nth-child(1)"
)
SIGN_IN = Selector(
    By.CSS_SELECTOR, "#articles > div > div.scope-indicator > p > a:nth-child(2)"
)

SELECTORS = {
    "hero": {
        "itself": Selector(By.CSS_SELECTOR, "#content > section.hero-section"),
        "heading title": ARTICLE_CATEGORY,
    },
    "breadcrumbs": {"breadcrumbs": BREADCRUMBS},
    "scope": {
        "article category introduction": ARTICLE_CATEGORY_INTRO,
        "total number of articles": TOTAL_NUMBER_OF_ARTICLES,
        "articles read counter": ARTICLES_TO_READ_COUNTER,
        "time to complete remaining chapters": TIME_TO_COMPLETE,
    },
    "list of articles": {"itself": LIST_OF_ARTICLES},
    "error reporting": {
        "itself": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "report page link": IS_THERE_ANYTHING_WRONG_WITH_THIS_PAGE_LINK,
    },
    "save progress": {"register link": REGISTER, "sign-in link": SIGN_IN},
}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    import copy

    all_except_save_progress = copy.copy(SELECTORS)
    all_except_save_progress.pop("save progress")
    check_for_expected_sections_elements(driver, all_except_save_progress)


def should_see_section(driver: WebDriver, name: str):
    check_for_section(driver, all_sections=SELECTORS, sought_section=name)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def should_not_see_section(driver: WebDriver, name: str):
    section = SELECTORS[name.lower()]
    for key, selector in section.items():
        check_if_element_is_not_visible(driver, selector, element_name=key)


def show_more(driver: WebDriver):
    button = find_element(driver, SHOW_MORE_BUTTON, element_name="Show more button")
    assert button.is_displayed()
    button.click()
    take_screenshot(driver, NAME + " after showing more")


def show_all_articles(driver: WebDriver):
    take_screenshot(driver, NAME + " before showing all articles")
    try:
        show_more_button = find_element(driver, SHOW_MORE_BUTTON, wait_for_it=False)
        max_clicks = 10
        counter = 0
        # click up to 11 times - see bug ED-2561
        while show_more_button.is_displayed() and counter <= max_clicks:
            show_more_button.click()
            counter += 1
        if counter > max_clicks:
            with assertion_msg(
                "'Show more' button didn't disappear after clicking on it"
                " for %d times",
                counter,
            ):
                assert counter == max_clicks
        take_screenshot(driver, NAME + " after showing all articles")
    except NoSuchElementException:
        logging.debug("Nothing to click as 'Show More' button is not visible")
