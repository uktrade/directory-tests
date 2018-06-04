# -*- coding: utf-8 -*-
"""ExRed Common Guidance Page Object."""
import logging

from selenium import webdriver
from selenium.webdriver import ActionChains

from registry.articles import get_article, get_articles
from utils import (
    assertion_msg,
    check_if_element_is_visible,
    find_element,
    find_elements,
    take_screenshot,
    wait_for_page_load_after_action,
)

NAME = "ExRed Common Guidance"
URL = None


RIBBON = {
    "itself": ".navigation-ribbon",
    "market research": ".navigation-ribbon a[href='/market-research/']",
    "customer insight": ".navigation-ribbon a[href='/customer-insight/']",
    "finance": ".navigation-ribbon a[href='/finance/']",
    "business planning": ".navigation-ribbon a[href='/business-planning/']",
    "getting paid": ".navigation-ribbon a[href='/getting-paid/']",
    "operations and compliance": ".navigation-ribbon a[href='/operations-and-compliance/']",
}
TOTAL_NUMBER_OF_ARTICLES = "dd.position > span.to"
ARTICLES_TO_READ_COUNTER = "dd.position > span.from"
TIME_TO_COMPLETE = "dd.time > span.value"
ARTICLES_LIST = "#js-paginate-list > li"
NEXT_CATEGORY_LINK = ""
FIRST_ARTICLE = "#js-paginate-list > li:nth-child(1) > a"

SCOPE_ELEMENTS = {
    "total number of articles": TOTAL_NUMBER_OF_ARTICLES,
    "articles read counter": ARTICLES_TO_READ_COUNTER,
    "time to complete remaining chapters": TIME_TO_COMPLETE,
}


def ribbon_should_be_visible(driver: webdriver):
    take_screenshot(driver, NAME + " Ribbon")
    for element_name, element_selector in RIBBON.items():
        logging.debug(
            "Looking for Ribbon '%s' element with '%s' selector",
            element_name,
            element_selector,
        )
        element = find_element(
            driver, by_css=element_selector, element_name=element_name
        )
        check_if_element_is_visible(element, element_name=element_name)


def ribbon_tile_should_be_highlighted(driver: webdriver, tile: str):
    tile_selector = RIBBON[tile.lower()]
    tile_link = find_element(driver, by_css=tile_selector)
    tile_class = tile_link.get_attribute("class")
    with assertion_msg(
        "It looks like '%s' tile is not active (it's class is %s)",
        tile,
        tile_class,
    ):
        assert tile_class == "active"


def correct_total_number_of_articles(driver: webdriver, category: str):
    expected = len(get_articles("guidance", category))
    total = find_element(
        driver,
        by_css=TOTAL_NUMBER_OF_ARTICLES,
        element_name="Total number of articles",
    )
    check_if_element_is_visible(total, element_name="Total number of articles")
    given = int(total.text)
    with assertion_msg(
        "Expected Total Number of Articles to read in Guidance '%s' "
        "category to be %d but got %s",
        category,
        expected,
        given,
    ):
        assert given == expected


def correct_article_read_counter(
    driver: webdriver, category: str, expected: int
):
    counter = find_element(
        driver,
        by_css=ARTICLES_TO_READ_COUNTER,
        element_name="Number of remaining articles to read",
        wait_for_it=False,
    )
    check_if_element_is_visible(
        counter, element_name="Number of remaining articles to read"
    )
    given = int(counter.text)
    with assertion_msg(
        "Expected Article Read Counter Guidance '%s' category to be %d but"
        " got %s",
        category,
        expected,
        given,
    ):
        assert given == expected


def check_if_correct_articles_are_displayed(driver: webdriver, category: str):
    """Check if all expected articles for given category are displayed and are
     on correct position.

    :param driver: selenium webdriver
    :param category: expected Guidance Article category
    """
    # extract displayed list of articles and their indexes
    articles = find_elements(driver, by_css=ARTICLES_LIST)
    given_articles = [
        (idx, article.find_element_by_tag_name("a").text)
        for idx, article in enumerate(articles)
    ]
    # check whether article is on the right position
    logging.debug("Given articles: %s", given_articles)
    for position, name in given_articles:
        expected_position = get_article("guidance", category, name).index
        with assertion_msg(
            "Expected article '%s' to be at position %d but found it at "
            "position no. %d ",
            name,
            expected_position,
            position,
        ):
            assert expected_position == position


def check_if_link_to_next_category_is_displayed(
    driver: webdriver, next_category: str
):
    """Check if link to the next Guidance category is displayed, except:
    the "last" Guidance category.

    :param driver: selenium webdriver
    :param next_category: Category for which "next" link should be visible
    """
    if next_category.lower() != "last":
        # TODO uncomment when link to the next category is implemented
        # link = driver.find_element_by_css_selector(NEXT_CATEGORY_LINK)
        # is_displayed = link.is_displayed()
        is_displayed = False
        with assertion_msg(
            "Found a link to the next category on the last Category page"
        ):
            assert not is_displayed
    else:
        # TODO uncomment when link to the next category is implemented
        # link = driver.find_element_by_css_selector(NEXT_CATEGORY_LINK)
        # is_displayed = link.is_displayed()
        is_displayed = True
        with assertion_msg("Link to the next category is not visible"):
            assert is_displayed


def check_elements_are_visible(driver: webdriver, elements: list):
    take_screenshot(driver, NAME)
    for element in elements:
        selector = SCOPE_ELEMENTS[element.lower()]
        page_element = find_element(
            driver, by_css=selector, element_name=element
        )
        if "firefox" not in driver.capabilities["browserName"].lower():
            logging.debug("Moving focus to '%s' element", element)
            action_chains = ActionChains(driver)
            action_chains.move_to_element(page_element)
            action_chains.perform()
        check_if_element_is_visible(page_element, element_name=element)


def open_first_article(driver: webdriver):
    first_article = find_element(
        driver,
        by_css=FIRST_ARTICLE,
        element_name="First article on list",
        wait_for_it=False,
    )
    check_if_element_is_visible(
        first_article, element_name="First article on list"
    )
    with wait_for_page_load_after_action(driver):
        first_article.click()
    take_screenshot(driver, "after opening first article")
