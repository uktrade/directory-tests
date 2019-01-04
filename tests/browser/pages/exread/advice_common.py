# -*- coding: utf-8 -*-
"""ExRed Common Advice Page Object."""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Selector,
    check_if_element_is_visible,
    find_element,
    find_elements,
    take_screenshot,
    wait_for_page_load_after_action,
    check_url,
    check_for_sections
)
from settings import EXRED_UI_URL

NAME = "Advice"
TYPE = "article list"
SERVICE = "Export Readiness"
URL = urljoin(EXRED_UI_URL, "advice/")
PAGE_TITLE = "Welcome to great.gov.uk"
NAMES = [
    "Create an export plan",
    "Find an export market",
    "Define route to market",
    "Get export finance and funding",
    "Manage payment for export orders",
    "Prepare to do business in a foreign country",
    "Manage legal and ethical compliance",
    "Prepare for export procedures and logistics",
]
URLs = {
    "create an export plan": urljoin(URL, "create-an-export-plan/"),
    "find an export market": urljoin(URL, "find-an-export-market/"),
    "define route to market": urljoin(URL, "define-route-to-market/"),
    "get export finance and funding": urljoin(URL, "get-export-finance-and-funding/"),
    "manage payment for export orders": urljoin(URL, "manage-payment-for-export-orders/"),
    "prepare to do business in a foreign country": urljoin(URL, "prepare-to-do-business-in-a-foreign-country/"),
    "manage legal and ethical compliance": urljoin(URL, "manage-legal-and-ethical-compliance/"),
    "prepare for export procedures and logistics": urljoin(URL, "prepare-for-export-procedures-and-logistics/"),
}


TOTAL_NUMBER_OF_ARTICLES = Selector(By.CSS_SELECTOR, "dd.position > span.to")
ARTICLES_TO_READ_COUNTER = Selector(By.CSS_SELECTOR, "dd.position > span.from")
TIME_TO_COMPLETE = Selector(By.CSS_SELECTOR, "dd.time > span.value")
ARTICLES_LIST = Selector(By.CSS_SELECTOR, "#js-paginate-list > li")
FIRST_ARTICLE = Selector(By.CSS_SELECTOR, "#js-paginate-list > li:nth-child(1) > a")

ARTICLE_COUNTER = Selector(By.ID, "hero-description")
ARTICLE_LINKS = Selector(
    By.CSS_SELECTOR, "#article-list-page li.article a", type=ElementType.LINK)
SELECTORS = {
    "hero": {
        "itself": Selector(By.ID, "hero"),
        "heading": Selector(By.ID, "hero-heading"),
        "description": Selector(By.ID, "hero-description"),
    },
    "breadcrumbs": {
        "itself": Selector(By.CSS_SELECTOR, "nav.breadcrumbs"),
        "links": Selector(By.CSS_SELECTOR, "nav.breadcrumbs a"),
    },
    "total number of articles": {
        "itself": ARTICLE_COUNTER,
    },
    "list of articles": {
        "itself": Selector(By.ID, "article-list-page"),
        "articles": ARTICLE_LINKS,
    },
    "error reporting": {
        "itself": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "link": Selector(By.ID, "error-reporting-section-contact-us"),
    },
}


def should_be_here(driver: WebDriver, *, page_name: str):
    take_screenshot(driver, PAGE_TITLE)
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)


def ribbon_should_be_visible(driver: WebDriver):
    take_screenshot(driver, NAME + " Ribbon")
    for element_name, element_selector in SELECTORS["ribbon"].items():
        logging.debug(
            "Looking for Ribbon '%s' element with '%s' selector",
            element_name,
            element_selector,
        )
        element = find_element(driver, element_selector, element_name=element_name)
        check_if_element_is_visible(element, element_name=element_name)


def ribbon_tile_should_be_highlighted(driver: WebDriver, tile: str):
    tile_selector = SELECTORS["ribbon"][tile.lower()]
    tile_link = find_element(driver, tile_selector)
    tile_class = tile_link.get_attribute("class")
    with assertion_msg(
        "It looks like '%s' tile is not active (it's class is %s)", tile, tile_class
    ):
        assert tile_class == "active"


def correct_total_number_of_articles(driver: WebDriver, category: str):
    expected = len(get_articles("advice", category))
    total = find_element(
        driver, TOTAL_NUMBER_OF_ARTICLES, element_name="Total number of articles"
    )
    check_if_element_is_visible(total, element_name="Total number of articles")
    given = int(total.text)
    with assertion_msg(
        "Expected Total Number of Articles to read in Advice '%s' "
        "category to be %d but got %s",
        category,
        expected,
        given,
    ):
        assert given == expected


def correct_article_read_counter(driver: WebDriver, category: str, expected: int):
    counter = find_element(
        driver,
        ARTICLES_TO_READ_COUNTER,
        element_name="Number of remaining articles to read",
        wait_for_it=False,
    )
    check_if_element_is_visible(
        counter, element_name="Number of remaining articles to read"
    )
    given = int(counter.text)
    with assertion_msg(
        "Expected Article Read Counter Advice '%s' category to be %d but" " got %s",
        category,
        expected,
        given,
    ):
        assert given == expected


def check_if_correct_articles_are_displayed(driver: WebDriver, category: str):
    """Check if all expected articles for given category are displayed and are
     on correct position.

    :param driver: selenium webdriver
    :param category: expected Advice Article category
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
        expected_position = get_article("advice", category, name).index
        with assertion_msg(
            "Expected article '%s' to be at position %d but found it at "
            "position no. %d ",
            name,
            expected_position,
            position,
        ):
            assert expected_position == position


def check_if_link_to_next_category_is_displayed(driver: WebDriver, next_category: str):
    """Check if link to the next Advice category is displayed, except:
    the "last" Advice category.

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


def check_elements_are_visible(driver: WebDriver, elements: list):
    take_screenshot(driver, NAME)
    for element in elements:
        selector = SELECTORS["scope elements"][element.lower()]
        page_element = find_element(driver, selector, element_name=element)
        if "firefox" not in driver.capabilities["browserName"].lower():
            logging.debug("Moving focus to '%s' element", element)
            action_chains = ActionChains(driver)
            action_chains.move_to_element(page_element)
            action_chains.perform()
        check_if_element_is_visible(page_element, element_name=element)


def open_first_article(driver: WebDriver):
    first_article = find_element(
        driver, FIRST_ARTICLE, element_name="First article on list", wait_for_it=False
    )
    check_if_element_is_visible(first_article, element_name="First article on list")
    with wait_for_page_load_after_action(driver):
        first_article.click()
    take_screenshot(driver, "after opening first article")
