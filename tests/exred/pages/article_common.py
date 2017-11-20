# -*- coding: utf-8 -*-
"""ExRed Common Articles Page Object."""
import logging

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains

from registry.articles import get_articles
from utils import assertion_msg, selenium_action, take_screenshot

NAME = "ExRed Common Articles"
URL = None

WORDS_PER_SECOND = 1.5  # Average word per second on screen
ARTICLE_TEXT = "#top"
INDICATORS_TEXT = "#top div.scope-indicator"
ARTICLE_NAME = "#top > h1"
TOTAL_NUMBER_OF_ARTICLES = "dd.position > span.to"
ARTICLES_TO_READ_COUNTER = "dd.position > span.from"
TIME_TO_COMPLETE = "dd.time span.value"
NEXT_ARTICLE_LINK = "#next-article-link"
SHARE_MENU = "ul.sharing-links"
SHOW_MORE_BUTTON = "#js-paginate-list-more"
GO_BACK_LINK = "#category-link"

SCOPE_ELEMENTS = {
    "total number of articles": TOTAL_NUMBER_OF_ARTICLES,
    "articles read counter": ARTICLES_TO_READ_COUNTER,
    "time to complete remaining chapters": TIME_TO_COMPLETE,
    "share menu": SHARE_MENU,
    "article name": ARTICLE_NAME
}


def correct_total_number_of_articles(
        driver: webdriver, group: str, category: str):
    expected = len(get_articles(group, category))
    total = driver.find_element_by_css_selector(TOTAL_NUMBER_OF_ARTICLES)
    with assertion_msg(
            "Total Number of Articles to read for %s '%s' category is "
            "not visible", group, category):
        assert total.is_displayed()
    given = int(total.text)
    with assertion_msg(
            "Expected Total Number of Articles to read in %s '%s' "
            "category to be %d but got %s", group, category, expected, given):
        assert given == expected


def correct_article_read_counter(driver: webdriver, expected: int):
    counter = driver.find_element_by_css_selector(ARTICLES_TO_READ_COUNTER)
    with assertion_msg("Article Read Counter is not visible"):
        assert counter.is_displayed()
    given = int(counter.text)
    with assertion_msg(
            "Expected Article Read Counter to be %d but got %s",
            expected, given):
        assert given == expected


def check_if_link_to_next_article_is_displayed(
        driver: webdriver, next_article: str):
    """Check if link to the next Guidance Article is displayed, except on
    the last one.

    :param driver: selenium webdriver
    :param next_article: Category for which "next" link should be visible
    """
    if next_article.lower() == "last":
        link = driver.find_element_by_css_selector(NEXT_ARTICLE_LINK)
        with assertion_msg(
                "Found a link to the next Article on '%s' page: '%s'",
                next_article, driver.current_url):
            assert not link.is_displayed()
    else:
        link = driver.find_element_by_css_selector(NEXT_ARTICLE_LINK)
        with assertion_msg(
                "Link to the next Article is not visible on '%s'",
                driver.current_url):
            assert link.is_displayed()
        with assertion_msg(
                "Expected to see a link to '%s' but got '%s'",
                next_article, link.text):
            assert link.text.lower() == next_article.lower()


def check_elements_are_visible(driver: webdriver, elements: list):
    take_screenshot(driver, NAME)
    for element in elements:
        selector = SCOPE_ELEMENTS[element.lower()]
        with selenium_action(
                driver, "Could not find '%s' on '%s' using '%s' selector",
                element, driver.current_url, selector):
            page_element = driver.find_element_by_css_selector(selector)
            if "firefox" not in driver.capabilities["browserName"].lower():
                logging.debug("Moving focus to '%s' element", element)
                action_chains = ActionChains(driver)
                action_chains.move_to_element(page_element)
                action_chains.perform()
        with assertion_msg("Expected to see '%s' but can't see it", element):
            assert page_element.is_displayed()


def show_all_articles(driver: webdriver):
    with selenium_action(
            driver, "Can't find 'Show more' button @'%s'", driver.current_url):
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


def go_to_article(driver: webdriver, title: str):
    with selenium_action(driver, "Could not find article: %s", title):
        article = driver.find_element_by_link_text(title)
        if "firefox" not in driver.capabilities["browserName"].lower():
            logging.debug("Moving focus to '%s' article link", title)
            action_chains = ActionChains(driver)
            action_chains.move_to_element(article)
            action_chains.perform()
    with assertion_msg(
            "Found a link to '%s' article but it's not visible", title):
        assert article.is_displayed()
    article.click()
    take_screenshot(driver, "After going to the '%s' Article".format(title))


def get_article_name(driver: webdriver) -> str:
    current_article = driver.find_element_by_css_selector(ARTICLE_NAME)
    return current_article.text


def should_see_article(driver: webdriver, name: str):
    current_article = get_article_name(driver)
    with assertion_msg(
            "Expected to see '%s' Article but got '%s'", name,
            current_article):
        assert current_article.lower() == name.lower()


def go_to_next_article(driver: webdriver):
    next_article = driver.find_element_by_css_selector(NEXT_ARTICLE_LINK)
    assert next_article.is_displayed()
    next_article.click()
    take_screenshot(driver, "After going to the next Article")


def should_not_see_link_to_next_article(driver: webdriver):
    try:
        next_article = driver.find_element_by_css_selector(NEXT_ARTICLE_LINK)
        with assertion_msg("Link to the next article is visible"):
            assert not next_article.is_displayed()
    except NoSuchElementException:
        logging.debug("As expected link to the next article, is not present")


def should_not_see_personas_end_page(driver: webdriver):
    """Check if Actor is stil on an Article page."""
    check_elements_are_visible(driver, ["article name"])


def go_back_to_article_list(driver: webdriver):
    with selenium_action(
            driver, "Could not find Go back link on '%s'", driver.current_url):
        go_back_link = driver.find_element_by_css_selector(GO_BACK_LINK)
    with assertion_msg("Go back link is not visible"):
        go_back_link.is_displayed()
    go_back_link.click()


def should_see_article_as_read(driver: webdriver, title: str):
    with selenium_action(driver, "Could not find article: %s", title):
        article = driver.find_element_by_link_text(title)
    with assertion_msg(
            "It looks like '%s' article is marked as unread", title):
        assert "article-read" in article.get_attribute("class")


def get_read_counter(driver: webdriver) -> int:
    with selenium_action(driver, "Could not find Article Read Counter"):
        counter = driver.find_element_by_css_selector(ARTICLES_TO_READ_COUNTER)
        if "firefox" not in driver.capabilities["browserName"].lower():
            logging.debug("Moving focus to Article Read Counter")
            action_chains = ActionChains(driver)
            action_chains.move_to_element(counter)
            action_chains.perform()
    with assertion_msg("Article Read Counter is not visible"):
        assert counter.is_displayed()
    return int(counter.text)


def get_time_to_complete(driver: webdriver) -> int:
    ttc = driver.find_element_by_css_selector(TIME_TO_COMPLETE)
    with assertion_msg("Time To Complete Reading Articles is not visible"):
        assert ttc.is_displayed()
    ttc_value = [int(word) for word in ttc.text.split() if word.isdigit()][0]
    return ttc_value


def filter_lines(lines_list):
    """BeautifulSoup returns \n as lines as well, we filter them out.
    It's a function because more filtering can be added later.
    """
    return filter(lambda x: x != '\n', lines_list)


def count_average_word_number_in_lines_list(lines_list, word_length=5):
    """Assume average word length, counts how many words in all the lines."""
    total_words = 0
    for line in lines_list:
        total_words += len(line)/word_length
    return total_words


def time_to_read_in_seconds(driver: webdriver):
    """Return time to read in minutes give an Article object."""
    article_text = driver.find_element_by_css_selector(ARTICLE_TEXT).text
    indicators_text = driver.find_element_by_css_selector(INDICATORS_TEXT).text
    only_article = article_text.replace(indicators_text, '')
    filtered_lines = filter_lines(only_article)
    total_words_count = count_average_word_number_in_lines_list(filtered_lines)
    return round(total_words_count / WORDS_PER_SECOND)
