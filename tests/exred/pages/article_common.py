# -*- coding: utf-8 -*-
"""ExRed Common Articles Page Object."""
import logging

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains

from registry.articles import get_articles
from utils import (
    assertion_msg,
    check_if_element_is_not_present,
    find_element,
    selenium_action,
    take_screenshot
)

NAME = "ExRed Common Articles"
URL = None
WORDS_PER_SECOND = 1.5  # Average word per second on screen

ARTICLE_NAME = "#top > h1"
ARTICLE_TEXT = "#top"
ARTICLES_TO_READ_COUNTER = "dd.position > span.from"
BREADCRUMBS = "p.breadcrumbs"
FEEDBACK_QUESTION = "#js-feedback > p"
FEEDBACK_RESULT = "#js-feedback-success"
GO_BACK_LINK = "#category-link"
INDICATORS_TEXT = "#top div.scope-indicator"
IS_THERE_ANYTHING_WRONG_WITH_THIS_PAGE_LINK = "section.error-reporting a"
NEXT_ARTICLE_LINK = "#next-article-link"
NOT_USEFUL_BUTTON = "#js-feedback-negative"
REGISTRATION_LINK = "#top > div > p > a:nth-child(1)"
SHARE_MENU = "ul.sharing-links"
SHOW_MORE_BUTTON = "#js-paginate-list-more"
SIGN_IN_LINK = "#top > div > p > a:nth-child(2)"
TIME_TO_COMPLETE = "dd.time span.value"
TOTAL_NUMBER_OF_ARTICLES = "dd.position > span.to"
USEFUL_BUTTON = "#js-feedback-positive"

SCOPE_ELEMENTS = {
    "total number of articles": TOTAL_NUMBER_OF_ARTICLES,
    "articles read counter": ARTICLES_TO_READ_COUNTER,
    "time to complete remaining chapters": TIME_TO_COMPLETE,
    "share menu": SHARE_MENU,
    "article name": ARTICLE_NAME
}

EXPECTED_ELEMENTS = {
    "breadcrumbs": BREADCRUMBS,
    "share menu": SHARE_MENU,
    "total number of articles": TOTAL_NUMBER_OF_ARTICLES,
    "articles read counter": ARTICLES_TO_READ_COUNTER,
    "time to complete remaining chapters": TIME_TO_COMPLETE,
    "article name": ARTICLE_NAME,
    "article text": ARTICLE_TEXT,
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
    try:
        show_more_button = driver.find_element_by_css_selector(SHOW_MORE_BUTTON)
        max_clicks = 10
        counter = 0
        # click up to 11 times - see bug ED-2561
        while show_more_button.is_displayed() and counter <= max_clicks:
            show_more_button.click()
            counter += 1
        if counter > max_clicks:
            with assertion_msg(
                    "'Show more' button didn't disappear after clicking on it"
                    " for %d times", counter):
                assert counter == max_clicks
        take_screenshot(driver, NAME + " after showing all articles")
    except NoSuchElementException:
        logging.debug("Nothing to click as 'Show More' button is not visible")


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
    take_screenshot(driver, "After going to the '{}' Article".format(title))


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


def get_total_articles(driver: webdriver) -> int:
    counter = driver.find_element_by_css_selector(TOTAL_NUMBER_OF_ARTICLES)
    with assertion_msg("Total Number or Articles to Read is not visible"):
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


def flag_as_useful(driver: webdriver):
    with selenium_action(
            driver, "Could not find the 'YES' feedback button using: %s",
            USEFUL_BUTTON):
        useful = driver.find_element_by_css_selector(USEFUL_BUTTON)
    assert useful.is_displayed()
    useful.click()
    take_screenshot(driver, "After telling us that Article was useful")


def flag_as_not_useful(driver: webdriver):
    with selenium_action(
            driver, "Could not find the 'NO' feedback button using: %s",
            NOT_USEFUL_BUTTON):
        not_useful = driver.find_element_by_css_selector(NOT_USEFUL_BUTTON)
    assert not_useful.is_displayed()
    not_useful.click()
    take_screenshot(driver, "After telling us that Article was not useful")


def should_not_see_feedback_widget(driver: webdriver):
    with selenium_action(
            driver, "Could not find all elements of feedback widget"):
        question = driver.find_element_by_css_selector(FEEDBACK_QUESTION)
        useful = driver.find_element_by_css_selector(USEFUL_BUTTON)
        not_useful = driver.find_element_by_css_selector(NOT_USEFUL_BUTTON)
    with assertion_msg(
            "Expected Feedback Widget to be hidden, but it's still visible"):
        assert not question.is_displayed()
        assert not useful.is_displayed()
        assert not not_useful.is_displayed()


def should_see_feedback_result(driver: webdriver):
    with selenium_action(
            driver, "Could not find the 'Thank you for the feedback' message"):
        result = driver.find_element_by_css_selector(FEEDBACK_RESULT)
    with assertion_msg(
            "Expected to be thanked for the Feedback, but can't see such "
            "message"):
        assert result.is_displayed()


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
