# -*- coding: utf-8 -*-
"""ExRed Common Export Readiness Page Object."""
import logging

from selenium import webdriver
from selenium.webdriver import ActionChains

from registry.articles import get_article, get_articles
from utils import (
    assertion_msg,
    check_if_element_is_visible,
    find_element,
    find_elements,
    take_screenshot
)

NAME = "ExRed Common Export Readiness"
URL = None


TOTAL_NUMBER_OF_ARTICLES = "dd.position > span.to"
ARTICLES_TO_READ_COUNTER = "dd.position > span.from"
TIME_TO_COMPLETE = "dd.time > span.value"
ARTICLES_LIST = "#js-paginate-list > li"

SCOPE_ELEMENTS = {
    "total number of articles": TOTAL_NUMBER_OF_ARTICLES,
    "articles read counter": ARTICLES_TO_READ_COUNTER,
    "time to complete remaining chapters": TIME_TO_COMPLETE
}


def correct_total_number_of_articles(driver: webdriver, category: str):
    expected = len(get_articles("export readiness", category))
    total = find_element(
        driver, by_css=TOTAL_NUMBER_OF_ARTICLES,
        element_name="Total number of articles", wait_for_it=False)
    check_if_element_is_visible(total, element_name="Total number of articles")
    given = int(total.text)
    with assertion_msg(
            "Expected Total Number of Export Readiness Articles to read for "
            "'%s' Exporter to be %d but got %s", category, expected, given):
        assert given == expected


def correct_article_read_counter(
        driver: webdriver, category: str, expected: int):
    counter = find_element(
        driver, by_css=ARTICLES_TO_READ_COUNTER,
        element_name="Remaining number of articles to read", wait_for_it=False)
    check_if_element_is_visible(
        counter, element_name="Remaining number of articles to read")
    given = int(counter.text)
    with assertion_msg(
            "Expected Export Readiness Article Read Counter for '%s' Exporter"
            " to be %d but got %s", category, expected, given):
        assert given == expected


def check_if_correct_articles_are_displayed(
        driver: webdriver, category: str):
    """Check if all expected articles for given category are displayed and are
     on correct position.

    :param driver: selenium webdriver
    :param category: expected Guidance Article category
    """
    # extract displayed list of articles and their indexes
    articles = find_elements(driver, by_css=ARTICLES_LIST)
    given_articles = [(idx, article.find_element_by_tag_name("a").text)
                      for idx, article in enumerate(articles)]
    # check whether article is on the right position
    logging.debug("Given articles: %s", given_articles)
    for position, name in given_articles:
        expected_position = get_article(
            "export readiness", category, name).index
        with assertion_msg(
                "Expected article '%s' to be at position %d but found it at "
                "position no. %d ", name, expected_position, position):
            assert expected_position == position


def check_elements_are_visible(driver: webdriver, elements: list):
    take_screenshot(driver, NAME)
    for element_name in elements:
        selector = SCOPE_ELEMENTS[element_name.lower()]
        page_element = find_element(
            driver, by_css=selector, element_name=element_name)
        if "firefox" not in driver.capabilities["browserName"].lower():
            logging.debug("Moving focus to '%s' element", element_name)
            action_chains = ActionChains(driver)
            action_chains.move_to_element(page_element)
            action_chains.perform()
        with assertion_msg(
                "Expected to see '%s' but can't see it", element_name):
            assert page_element.is_displayed()
