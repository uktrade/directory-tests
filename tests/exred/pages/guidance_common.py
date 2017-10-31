# -*- coding: utf-8 -*-
"""ExRed Common Guidance Page Object."""
import logging

from selenium import webdriver

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
    given = int(driver.find_element_by_css_selector(TOTAL_NUMBER_OF_ARTICLES).text)
    with assertion_msg(
            "Expected Total Number of Articles to read in Guidance '%s' "
            "category to be %d but got %s", category, expected, given):
        assert given == expected


def correct_article_read_counter(
        driver: webdriver, category: str, expected: int):
    given = int(driver.find_element_by_css_selector(ARTICLES_TO_READ_COUNTER).text)
    with assertion_msg(
            "Expected Article Read Counter Guidance '%s' category to be %d but"
            " got %s", category, expected, given):
        assert given == expected
