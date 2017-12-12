# -*- coding: utf-8 -*-
"""ExRed Article List Page Object."""
import logging

from selenium import webdriver

from utils import (
    assertion_msg,
    check_if_element_is_not_present,
    find_element,
    take_screenshot
)

NAME = "ExRed Article List"
URL = None

ARTICLE_CATEGORY = "#content > section h1.title"
BREADCRUMBS = "p.breadcrumbs"
ARTICLE_CATEGORY_INTRO = "div.section-intro"
LIST_OF_ARTICLES = "#js-paginate-list"
TOTAL_NUMBER_OF_ARTICLES = "dd.position > span.to"
ARTICLES_TO_READ_COUNTER = "dd.position > span.from"
TIME_TO_COMPLETE = "dd.time span.value"
SHOW_MORE_BUTTON = "#js-paginate-list-more"
REGISTRATION_LINK = "#articles p.register > a:nth-child(1)"
SIGN_IN_LINK = "#articles p.register > a:nth-child(2)"
IS_THERE_ANYTHING_WRONG_WITH_THIS_PAGE_LINK = "section.error-reporting a"

EXPECTED_ELEMENTS = {
    "article category name": ARTICLE_CATEGORY,
    "breadcrumbs": BREADCRUMBS,
    "article category introduction": ARTICLE_CATEGORY_INTRO,
    "total number of articles": TOTAL_NUMBER_OF_ARTICLES,
    "articles read counter": ARTICLES_TO_READ_COUNTER,
    "time to complete remaining chapters": TIME_TO_COMPLETE,
    "list of articles": LIST_OF_ARTICLES,
    "report page link": IS_THERE_ANYTHING_WRONG_WITH_THIS_PAGE_LINK
}


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    for element_name, element_selector in EXPECTED_ELEMENTS.items():
        element = find_element(driver, by_css=element_selector)
        with assertion_msg(
                "It looks like '%s' element is not visible on %s",
                element_name, NAME):
            assert element.is_displayed()
    logging.debug("All expected elements are visible on '%s' page", NAME)


def go_to_registration(driver: webdriver):
    registration_link = find_element(driver, by_css=REGISTRATION_LINK)
    registration_link.click()


def go_to_sign_in(driver: webdriver):
    sign_in_link = find_element(driver, by_css=SIGN_IN_LINK)
    sign_in_link.click()


def should_not_see_link_to_register(driver: webdriver):
    check_if_element_is_not_present(
        driver, by_css=REGISTRATION_LINK, element_name="Registration link")


def should_not_see_link_to_sign_in(driver: webdriver):
    check_if_element_is_not_present(
        driver, by_css=SIGN_IN_LINK, element_name="Sign in link")
