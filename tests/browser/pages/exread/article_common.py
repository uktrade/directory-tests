# -*- coding: utf-8 -*-
"""ExRed Common Articles Page Object."""
import logging
import time
from typing import List
from urllib import parse as urlparse

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    AssertionExecutor,
    Selector,
    assertion_msg,
    check_for_expected_sections_elements,
    check_for_section,
    check_for_sections,
    check_if_element_is_not_present,
    check_if_element_is_not_visible,
    check_if_element_is_visible,
    find_element,
    find_elements,
    selenium_action,
    take_screenshot,
    wait_for_page_load_after_action,
)
from registry.articles import get_articles

NAME = "Article"
SERVICE = "Export Readiness"
TYPE = "article"
URL = None
WORDS_PER_SECOND = 1.5  # Average word per second on screen

ARTICLE_NAME = Selector(By.CSS_SELECTOR, "#top h1")
ARTICLE_TEXT = Selector(By.ID, "top")
ARTICLES_TO_READ_COUNTER = Selector(By.CSS_SELECTOR, "dd.position > span.from")
BREADCRUMBS = Selector(By.CSS_SELECTOR, "div.breadcrumbs")
FEEDBACK_QUESTION = Selector(By.CSS_SELECTOR, "#js-feedback > p")
FEEDBACK_RESULT = Selector(By.ID, "js-feedback-success")
GO_BACK_LINK = Selector(By.ID, "category-link")
INDICATORS_TEXT = Selector(By.CSS_SELECTOR, "div.scope-indicator")
IS_THERE_ANYTHING_WRONG_WITH_THIS_PAGE_LINK = Selector(
    By.CSS_SELECTOR, "section.error-reporting a"
)
NEXT_ARTICLE_LINK = Selector(By.ID, "next-article-link")
NOT_USEFUL_BUTTON = Selector(By.ID, "js-feedback-negative")
REGISTRATION_LINK = Selector(
    By.CSS_SELECTOR, "#content div.article-container p.register > a:nth-child(1)"
)
READ_ARTICLES = Selector(By.CSS_SELECTOR, "a.article-read")
SHARE_MENU = Selector(By.CSS_SELECTOR, "ul.sharing-links")
SHOW_MORE_BUTTON = Selector(By.ID, "js-paginate-list-more")
SIGN_IN_LINK = Selector(
    By.CSS_SELECTOR, "#content div.article-container p.register > a:nth-child(2)"
)
TIME_TO_COMPLETE = Selector(By.CSS_SELECTOR, "dd.time span.value")
TOTAL_NUMBER_OF_ARTICLES = Selector(By.CSS_SELECTOR, "dd.position > span.to")
USEFUL_BUTTON = Selector(By.ID, "js-feedback-positive")
FACEBOOK_BUTTON = Selector(By.ID, "share-facebook")
LINKEDIN_BUTTON = Selector(By.ID, "share-linkedin")
TWITTER_BUTTON = Selector(By.ID, "share-twitter")
EMAIL_BUTTON = Selector(By.ID, "share-email")
REGISTER = Selector(By.CSS_SELECTOR, "div.article-container p.register a:nth-child(1)")
SIGN_IN = Selector(By.CSS_SELECTOR, "div.article-container p.register a:nth-child(2)")

SHARE_BUTTONS = {
    "itself": SHARE_MENU,
    "facebook": FACEBOOK_BUTTON,
    "twitter": TWITTER_BUTTON,
    "linkedin": LINKEDIN_BUTTON,
    "email": EMAIL_BUTTON,
}

SELECTORS = {
    "share buttons": SHARE_BUTTONS,
    "save progress": {"register link": REGISTER, "sign-in link": SIGN_IN},
    "breadcrumbs": {"breadcrumbs": BREADCRUMBS},
    "scope": {
        "total number of articles": TOTAL_NUMBER_OF_ARTICLES,
        "articles read counter": ARTICLES_TO_READ_COUNTER,
        "time to complete remaining chapters": TIME_TO_COMPLETE,
    },
    "article": {"article name": ARTICLE_NAME, "article text": ARTICLE_TEXT},
    "feedback": {
        "not useful button": NOT_USEFUL_BUTTON,
        "useful button": USEFUL_BUTTON,
    },
    "error reporting": {
        "itself": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "report page link": IS_THERE_ANYTHING_WRONG_WITH_THIS_PAGE_LINK,
    },
}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    import copy

    all_except_save_progress = copy.copy(SELECTORS)
    all_except_save_progress.pop("save progress")
    check_for_expected_sections_elements(driver, all_except_save_progress)


def should_see_section(driver: WebDriver, name: str):
    check_for_section(driver, SELECTORS, sought_section=name)


def should_see_sections(executor: AssertionExecutor, names: List[str]):
    check_for_sections(executor, all_sections=SELECTORS, sought_sections=names)


def should_not_see_section(driver: WebDriver, name: str):
    section = SELECTORS[name.lower()]
    for key, selector in section.items():
        check_if_element_is_not_visible(driver, selector, element_name=key)


def correct_total_number_of_articles(driver: WebDriver, group: str, category: str):
    expected = len(get_articles(group, category))
    total = find_element(
        driver,
        TOTAL_NUMBER_OF_ARTICLES,
        element_name="Total number of articles",
        wait_for_it=False,
    )
    check_if_element_is_visible(total, element_name="Total number of articles")
    given = int(total.text)
    with assertion_msg(
        "Expected Total Number of Articles to read in %s '%s' "
        "category to be %d but got %s",
        group,
        category,
        expected,
        given,
    ):
        assert given == expected


def correct_article_read_counter(driver: WebDriver, expected: int):
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
        "Expected Article Read Counter to be %d but got %s", expected, given
    ):
        assert given == expected


def check_if_link_to_next_article_is_displayed(driver: WebDriver, next_article: str):
    """Check if link to the next Advice Article is displayed, except on
    the last one.

    :param driver: selenium webdriver
    :param next_article: Category for which "next" link should be visible
    """
    name = "Link to the next article"
    link = find_element(driver, NEXT_ARTICLE_LINK, element_name=name)
    check_if_element_is_visible(link, element_name=name)
    if next_article.lower() != "last":
        with assertion_msg(
            "Expected to see a link to '%s' but got '%s'", next_article, link.text
        ):
            assert link.text.lower() == next_article.lower()


def go_to_article(driver: WebDriver, title: str):
    with selenium_action(driver, "Could not find article: %s", title):
        article = driver.find_element_by_link_text(title)
        if "firefox" not in driver.capabilities["browserName"].lower():
            logging.debug("Moving focus to '%s' article link", title)
            action_chains = ActionChains(driver)
            action_chains.move_to_element(article)
            action_chains.perform()
    check_if_element_is_visible(article, element_name=title)
    with wait_for_page_load_after_action(driver):
        article.click()
    take_screenshot(driver, "After going to the '{}' Article".format(title))


def get_article_name(driver: WebDriver) -> str:
    current_article = find_element(driver, ARTICLE_NAME, element_name="Article name")
    return current_article.text


def should_see_article(driver: WebDriver, name: str):
    current_article = get_article_name(driver)
    with assertion_msg(
        "Expected to see '%s' Article but got '%s'", name, current_article
    ):
        assert current_article.lower() == name.lower()


def go_to_next_article(driver: WebDriver):
    next_article = find_element(
        driver,
        NEXT_ARTICLE_LINK,
        element_name="Link to the next article",
        wait_for_it=False,
    )
    check_if_element_is_visible(next_article, element_name="Link to the next article")
    with wait_for_page_load_after_action(driver):
        next_article.click()
    take_screenshot(driver, "After going to the next Article")


def should_not_see_link_to_next_article(driver: WebDriver):
    check_if_element_is_not_visible(
        driver, NEXT_ARTICLE_LINK, element_name="Link to the next article"
    )


def go_back_to_article_list(driver: WebDriver):
    element_name = "Go Back link"
    go_back_link = find_element(
        driver, GO_BACK_LINK, element_name=element_name, wait_for_it=False
    )
    check_if_element_is_visible(go_back_link, element_name)
    with wait_for_page_load_after_action(driver):
        go_back_link.click()


def should_see_article_as_read(driver: WebDriver, title: str):
    article = driver.find_element_by_link_text(title)
    with assertion_msg("It looks like '%s' article is marked as unread", title):
        assert "article-read" in article.get_attribute("class")


def get_read_counter(driver: WebDriver) -> int:
    element_name = "Article read counter"
    counter = find_element(
        driver, ARTICLES_TO_READ_COUNTER, element_name=element_name, wait_for_it=False
    )
    if "firefox" not in driver.capabilities["browserName"].lower():
        logging.debug("Moving focus to Article Read Counter")
        action_chains = ActionChains(driver)
        action_chains.move_to_element(counter)
        action_chains.perform()
    check_if_element_is_visible(counter, element_name=element_name)
    return int(counter.text)


def get_total_articles(driver: WebDriver) -> int:
    element_name = "Total Number or Articles to Read"
    counter = find_element(
        driver, TOTAL_NUMBER_OF_ARTICLES, element_name=element_name, wait_for_it=False
    )
    check_if_element_is_visible(counter, element_name)
    return int(counter.text)


def get_time_to_complete(driver: WebDriver) -> int:
    element_name = "Time to complete reading remaining articles"
    ttc = find_element(driver, TIME_TO_COMPLETE, element_name=element_name)
    check_if_element_is_visible(ttc, element_name)
    ttc_value = [int(word) for word in ttc.text.split() if word.isdigit()][0]
    return ttc_value


def filter_lines(lines_list):
    """BeautifulSoup returns \n as lines as well, we filter them out.
    It's a function because more filtering can be added later.
    """
    return filter(lambda x: x != "\n", lines_list)


def count_average_word_number_in_lines_list(lines_list, word_length=5):
    """Assume average word length, counts how many words in all the lines."""
    total_words = 0
    for line in lines_list:
        total_words += len(line) / word_length
    return total_words


def time_to_read_in_seconds(driver: WebDriver):
    """Return time to read in minutes give an Article object."""
    article_text = find_element(driver, ARTICLE_TEXT, wait_for_it=False).text
    filtered_lines = filter_lines(article_text)
    total_words_count = count_average_word_number_in_lines_list(filtered_lines)
    return round(total_words_count / WORDS_PER_SECOND)


def flag_as_useful(driver: WebDriver):
    element_name = "Yes - this article was useful button"
    useful = find_element(
        driver, USEFUL_BUTTON, element_name=element_name, wait_for_it=False
    )
    check_if_element_is_visible(useful, element_name)
    useful.click()
    take_screenshot(driver, "After telling us that Article was useful")


def flag_as_not_useful(driver: WebDriver):
    element_name = "No - this article was not useful button"
    not_useful = find_element(driver, NOT_USEFUL_BUTTON, element_name=element_name)
    check_if_element_is_visible(not_useful, element_name)
    not_useful.click()
    take_screenshot(driver, "After telling us that Article was not useful")


def should_not_see_feedback_widget(driver: WebDriver):
    time.sleep(1)
    check_if_element_is_not_visible(
        driver, FEEDBACK_QUESTION, element_name="Feedback question", wait_for_it=False
    )
    check_if_element_is_not_visible(
        driver, USEFUL_BUTTON, element_name="Useful button", wait_for_it=False
    )
    check_if_element_is_not_visible(
        driver, NOT_USEFUL_BUTTON, element_name="Not useful button", wait_for_it=False
    )


def should_see_feedback_result(driver: WebDriver):
    element_name = "Feedback result (thank you message)"
    result = find_element(driver, FEEDBACK_RESULT, element_name=element_name)
    check_if_element_is_visible(result, element_name)


def go_to_registration(driver: WebDriver):
    registration_link = find_element(driver, REGISTRATION_LINK)
    with wait_for_page_load_after_action(driver):
        registration_link.click()


def go_to_sign_in(driver: WebDriver):
    sign_in_link = find_element(driver, SIGN_IN_LINK)
    with wait_for_page_load_after_action(driver):
        sign_in_link.click()


def should_not_see_link_to_register(driver: WebDriver):
    check_if_element_is_not_present(
        driver, REGISTRATION_LINK, element_name="Registration link"
    )


def should_not_see_link_to_sign_in(driver: WebDriver):
    check_if_element_is_not_present(driver, SIGN_IN_LINK, element_name="Sign in link")


def get_read_articles(driver: WebDriver) -> list:
    return [art.text for art in find_elements(driver, READ_ARTICLES)]


def check_if_link_opens_new_tab(driver: WebDriver, social_media: str):
    share_button_selector = SHARE_BUTTONS[social_media.lower()]
    share_button = find_element(driver, share_button_selector)
    target = share_button.get_attribute("target")
    with assertion_msg(
        "Expected link to '%s' share page to open in new tab, but instead "
        "found a link with target attribute set to '%s'",
        social_media,
        target,
    ):
        assert target == "_blank"


def check_if_link_opens_email_client(driver: WebDriver):
    share_button_selector = SHARE_BUTTONS["email"]
    share_button = find_element(driver, share_button_selector)
    href = share_button.get_attribute("href")
    with assertion_msg(
        "Expected the 'share via email' link to open in Email Client, but "
        "got a invalid link: %s",
        href,
    ):
        assert href.startswith("mailto:")


def check_share_via_email_link_details(
    driver: WebDriver, expected_subject: str, expected_body: str
):
    share_button_selector = SHARE_BUTTONS["email"]
    share_button = find_element(driver, share_button_selector)
    href = share_button.get_attribute("href")
    parsed_url = urlparse.urlparse(href)
    query_parameters = urlparse.parse_qs(parsed_url.query)
    subject = query_parameters["subject"][0]
    body = query_parameters["body"][0]
    with assertion_msg(
        "Expected 'share via email' link to contain message body '%s' but "
        "got '%s' instead",
        expected_body,
        body,
    ):
        assert body == expected_body
    with assertion_msg(
        "Expected 'share via email' link's message subject to contain "
        "Article title '%s' but got '%s' instead",
        expected_subject,
        subject,
    ):
        assert expected_subject in subject


def share_via(driver: WebDriver, social_media: str):
    share_button_selector = SHARE_BUTTONS[social_media.lower()]
    share_button = find_element(driver, share_button_selector)
    href = share_button.get_attribute("href")
    logging.debug("Opening 'Share on %s' link '%s' in the same tab", social_media, href)
    driver.get(href)
