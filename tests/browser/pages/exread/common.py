# -*- coding: utf-8 -*-
"""ExRed Common Export Readiness Page Object."""
import logging
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    assertion_msg,
    check_if_element_is_visible,
    find_element,
    find_elements,
    Selector,
    check_for_sections,
    AssertionExecutor
)
from registry.articles import get_article, get_articles

NAME = "ExRed Common Export Readiness"
URL = None


TOTAL_NUMBER_OF_ARTICLES = Selector(By.CSS_SELECTOR, "dd.position > span.to")
ARTICLES_TO_READ_COUNTER = Selector(By.CSS_SELECTOR, "dd.position > span.from")
TIME_TO_COMPLETE = Selector(By.CSS_SELECTOR, "dd.time > span.value")
ARTICLES_LIST = Selector(By.CSS_SELECTOR, "#js-paginate-list > li")

SELECTORS = {
    "general": {
        "total number of articles": TOTAL_NUMBER_OF_ARTICLES,
        "articles read counter": ARTICLES_TO_READ_COUNTER,
        "time to complete remaining chapters": TIME_TO_COMPLETE,
    }
}


def correct_total_number_of_articles(driver: WebDriver, category: str):
    expected = len(get_articles("export readiness", category))
    total = find_element(
        driver,
        TOTAL_NUMBER_OF_ARTICLES,
        element_name="Total number of articles",
        wait_for_it=False,
    )
    check_if_element_is_visible(total, element_name="Total number of articles")
    given = int(total.text)
    with assertion_msg(
        "Expected Total Number of Export Readiness Articles to read for "
        "'%s' Exporter to be %d but got %s",
        category,
        expected,
        given,
    ):
        assert given == expected


def correct_article_read_counter(driver: WebDriver, category: str, expected: int):
    counter = find_element(
        driver,
        ARTICLES_TO_READ_COUNTER,
        element_name="Remaining number of articles to read",
        wait_for_it=False,
    )
    check_if_element_is_visible(
        counter, element_name="Remaining number of articles to read"
    )
    given = int(counter.text)
    with assertion_msg(
        "Expected Export Readiness Article Read Counter for '%s' Exporter"
        " to be %d but got %s",
        category,
        expected,
        given,
    ):
        assert given == expected


def check_if_correct_articles_are_displayed(driver: WebDriver, category: str):
    """Check if all expected articles for given category are displayed and are
     on correct position.

    :param driver: selenium webdriver
    :param category: expected Guidance Article category
    """
    # extract displayed list of articles and their indexes
    articles = find_elements(driver, ARTICLES_LIST)
    given_articles = [
        (idx, article.find_element_by_tag_name("a").text)
        for idx, article in enumerate(articles)
    ]
    # check whether article is on the right position
    logging.debug("Given articles: %s", given_articles)
    for position, name in given_articles:
        expected_position = get_article("export readiness", category, name).index
        with assertion_msg(
            "Expected article '%s' to be at position %d but found it at "
            "position no. %d ",
            name,
            expected_position,
            position,
        ):
            assert expected_position == position


def should_see_sections(executor: AssertionExecutor, names: List[str]):
    check_for_sections(executor, all_sections=SELECTORS, sought_sections=names)
