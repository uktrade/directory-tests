# -*- coding: utf-8 -*-
"""ExRed Article List Page Object."""
import logging

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from pages.common_actions import (
    assertion_msg,
    check_for_expected_sections_elements,
    check_for_section,
    check_if_element_is_not_present,
    check_if_element_is_not_visible,
    find_element,
    take_screenshot,
    wait_for_page_load_after_action,
)

NAME = "ExRed Article List"
URL = None

SHOW_MORE_BUTTON = "#js-paginate-list-more"
ARTICLE_CATEGORY = "#content > section h1.title"
BREADCRUMBS = "p.breadcrumbs"
ARTICLE_CATEGORY_INTRO = "div.section-intro"
LIST_OF_ARTICLES = "#js-paginate-list"
TOTAL_NUMBER_OF_ARTICLES = "dd.position > span.to"
ARTICLES_TO_READ_COUNTER = "dd.position > span.from"
TIME_TO_COMPLETE = "dd.time span.value"
REGISTRATION_LINK = "#articles p.register > a:nth-child(1)"
SIGN_IN_LINK = "#articles p.register > a:nth-child(2)"
IS_THERE_ANYTHING_WRONG_WITH_THIS_PAGE_LINK = "section.error-reporting a"
REGISTER = "#articles > div > div.scope-indicator > p > a:nth-child(1)"
SIGN_IN = "#articles > div > div.scope-indicator > p > a:nth-child(2)"

SECTIONS = {
    "hero": {
        "itself": "#content > section.hero-section",
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
        "itself": "section.error-reporting",
        "report page link": IS_THERE_ANYTHING_WRONG_WITH_THIS_PAGE_LINK,
    },
    "save progress": {"register link": REGISTER, "sign-in link": SIGN_IN},
}


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    import copy

    all_except_save_progress = copy.copy(SECTIONS)
    all_except_save_progress.pop("save progress")
    check_for_expected_sections_elements(driver, all_except_save_progress)


def should_see_section(driver: webdriver, name: str):
    check_for_section(driver, all_sections=SECTIONS, sought_section=name)


def should_not_see_section(driver: webdriver, name: str):
    section = SECTIONS[name.lower()]
    for key, selector in section.items():
        check_if_element_is_not_visible(
            driver, by_css=selector, element_name=key
        )


def go_to_registration(driver: webdriver):
    registration_link = find_element(driver, by_css=REGISTRATION_LINK)
    with wait_for_page_load_after_action(driver):
        registration_link.click()


def go_to_sign_in(driver: webdriver):
    sign_in_link = find_element(driver, by_css=SIGN_IN_LINK)
    with wait_for_page_load_after_action(driver):
        sign_in_link.click()


def should_not_see_link_to_register(driver: webdriver):
    check_if_element_is_not_present(
        driver, by_css=REGISTRATION_LINK, element_name="Registration link"
    )


def should_not_see_link_to_sign_in(driver: webdriver):
    check_if_element_is_not_present(
        driver, by_css=SIGN_IN_LINK, element_name="Sign in link"
    )


def show_more(driver: webdriver):
    button = find_element(
        driver, by_css=SHOW_MORE_BUTTON, element_name="Show more button"
    )
    assert button.is_displayed()
    button.click()
    take_screenshot(driver, NAME + " after showing more")


def show_all_articles(driver: webdriver):
    take_screenshot(driver, NAME + " before showing all articles")
    try:
        show_more_button = find_element(
            driver, by_css=SHOW_MORE_BUTTON, wait_for_it=False
        )
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
