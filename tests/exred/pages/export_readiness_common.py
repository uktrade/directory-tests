# -*- coding: utf-8 -*-
"""ExRed Common Export Readiness Page Object."""
import logging

from selenium import webdriver

from registry.articles import get_articles
from utils import assertion_msg, take_screenshot

NAME = "ExRed Common Export Readiness"
URL = None


TOTAL_NUMBER_OF_ARTICLES = "#articles div.scope-indicator dd.position > span.to"
ARTICLES_TO_READ_COUNTER = "#articles div.scope-indicator dd.position > span.from"
TIME_TO_COMPLETE = "#articles div.scope-indicator dd.time > span.value"
SHOW_MORE_BUTTON = "#js-paginate-list-more"
ARTICLES_LIST = "#js-paginate-list > li"

SCOPE_ELEMENTS = {
    "total number of articles": TOTAL_NUMBER_OF_ARTICLES,
    "articles read counter": ARTICLES_TO_READ_COUNTER,
    "time to complete remaining chapters": TIME_TO_COMPLETE
}


def correct_total_number_of_articles(driver: webdriver, category: str):
    expected = len(get_articles("export readiness", category))
    total = driver.find_element_by_css_selector(TOTAL_NUMBER_OF_ARTICLES)
    with assertion_msg(
            "Total Number of Export Readiness Articles to read for '%s' "
            "Exporter is not visible", category):
        assert total.is_displayed()
    given = int(total.text)
    with assertion_msg(
            "Expected Total Number of Export Readiness Articles to read for "
            "'%s' Exporter to be %d but got %s", category, expected, given):
        assert given == expected


def correct_article_read_counter(
        driver: webdriver, category: str, expected: int):
    counter = driver.find_element_by_css_selector(ARTICLES_TO_READ_COUNTER)
    with assertion_msg(
            "Export Readiness Article Read Counter for '%s' Exporter is not "
            "visible", category):
        assert counter.is_displayed()
    given = int(counter.text)
    with assertion_msg(
            "Expected Export Readiness Article Read Counter for '%s' Exporter"
            " to be %d but got %s", category, expected, given):
        assert given == expected


def show_all_articles(driver: webdriver):
    show_more_button = driver.find_element_by_css_selector(SHOW_MORE_BUTTON)
    max_clicks = 10
    counter = 0
    # click up to 11 times - see bug ED-2561
    while show_more_button.is_displayed() and counter <= max_clicks:
        show_more_button.click()
        counter += 1
    if counter > max_clicks:
        with assertion_msg(
                "'Show more' button didn't disappear after clicking on it for"
                " %d times", counter):
            assert counter == max_clicks
    take_screenshot(driver, NAME + " after showing all articles")


def check_if_correct_articles_are_displayed(
        driver: webdriver, category: str):
    """Check if all expected articles for given category are displayed and are
     on correct position.

    :param driver: selenium webdriver
    :param category: expected Guidance Article category
    """
    expected_list = get_articles("export readiness", category.lower())
    # convert list of dict to a simpler dict, which will help in comparison
    expected_articles = {}
    for article in expected_list:
        expected_articles.update(article)
    show_all_articles(driver)
    # extract displayed list of articles and their indexes
    articles = driver.find_elements_by_css_selector(ARTICLES_LIST)
    given_articles = [(idx+1, article.find_element_by_tag_name("a").text)
                      for idx, article in enumerate(articles)]
    # check whether article is on the right position
    logging.debug("Expected articles: %s", expected_articles)
    logging.debug("Given articles: %s", given_articles)
    for position, name in given_articles:
        expected_position = expected_articles[name.lower()]["index"]
        with assertion_msg(
                "Expected article '%s' to be at position %d but found it at "
                "position no. %d ", name, expected_position, position):
            assert expected_position == position
