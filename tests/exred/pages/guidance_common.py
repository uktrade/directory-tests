# -*- coding: utf-8 -*-
"""ExRed Common Guidance Page Object."""
import logging

from selenium import webdriver
from selenium.webdriver import ActionChains

from registry.articles import get_articles
from utils import assertion_msg, selenium_action, take_screenshot

NAME = "ExRed Common Guidance"
URL = None


RIBBON = {
    "itself": ".navigation-ribbon",
    "market research": ".navigation-ribbon a[href='/market-research']",
    "customer insight": ".navigation-ribbon a[href='/customer-insight']",
    "finance": ".navigation-ribbon a[href='/finance']",
    "business planning": ".navigation-ribbon a[href='/business-planning']",
    "getting paid": ".navigation-ribbon a[href='/getting-paid']",
    "operations and compliance": ".navigation-ribbon a[href='/operations-and-compliance']"
}
TOTAL_NUMBER_OF_ARTICLES = "#articles div.scope-indicator dd.position > span.to"
ARTICLES_TO_READ_COUNTER = "#articles div.scope-indicator dd.position > span.from"
TIME_TO_COMPLETE = "#articles div.scope-indicator dd.time > span.value"
SHOW_MORE_BUTTON = "#js-paginate-list-more"
ARTICLES_LIST = "#js-paginate-list > li"
NEXT_CATEGORY_LINK = ""

SCOPE_ELEMENTS = {
    "total number of articles": TOTAL_NUMBER_OF_ARTICLES,
    "articles read counter": ARTICLES_TO_READ_COUNTER,
    "time to complete remaining chapters": TIME_TO_COMPLETE
}


def ribbon_should_be_visible(driver: webdriver):
    for element_name, element_selector in RIBBON.items():
        logging.debug(
            "Looking for Ribbon '%s' element with '%s' selector",
            element_name, element_selector)
        with selenium_action(
                driver, "Could not find '%s' using '%s'", element_name,
                element_selector):
            element = driver.find_element_by_css_selector(element_selector)
        with assertion_msg(
                "It looks like '%s' is not visible", element_name):
            assert element.is_displayed()
    take_screenshot(driver, NAME + " Ribbon")


def ribbon_tile_should_be_highlighted(driver: webdriver, tile: str):
    tile_selector = RIBBON[tile.lower()]
    with selenium_action(driver, "Could not find '%s' tile", tile):
        tile_link = driver.find_element_by_css_selector(tile_selector)
        tile_class = tile_link.get_attribute("class")
    with assertion_msg(
            "It looks like '%s' tile is not active (it's class is %s)",
            tile, tile_class):
        assert tile_class == "active"


def correct_total_number_of_articles(driver: webdriver, category: str):
    expected = len(get_articles("guidance", category))
    total = driver.find_element_by_css_selector(TOTAL_NUMBER_OF_ARTICLES)
    with assertion_msg(
            "Total Number of Articles to read for Guidance '%s' category is "
            "not visible", category):
        assert total.is_displayed()
    given = int(total.text)
    with assertion_msg(
            "Expected Total Number of Articles to read in Guidance '%s' "
            "category to be %d but got %s", category, expected, given):
        assert given == expected


def correct_article_read_counter(
        driver: webdriver, category: str, expected: int):
    counter = driver.find_element_by_css_selector(ARTICLES_TO_READ_COUNTER)
    with assertion_msg(
            "Article Read Counter for Guidance '%s' category is not visible",
            category):
        assert counter.is_displayed()
    given = int(counter.text)
    with assertion_msg(
            "Expected Article Read Counter Guidance '%s' category to be %d but"
            " got %s", category, expected, given):
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
    expected_list = get_articles("guidance", category.lower())
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


def check_if_link_to_next_category_is_displayed(
        driver: webdriver, next_category: str):
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
                "Found a link to the next category on the last Category page"):
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
        with selenium_action(
                driver, "Could not find '%s' on '%s' using '%s' selector",
                element, driver.current_url, selector):
            page_element = driver.find_element_by_css_selector(selector)
            action_chains = ActionChains(driver)
            action_chains.move_to_element(page_element)
            action_chains.perform()
        with assertion_msg("Expected to see '%s' but can't see it", element):
            assert page_element.is_displayed()
