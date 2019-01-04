# -*- coding: utf-8 -*-
"""ExRed Common Articles Page Object."""
import logging
from typing import List
from urllib import parse as urlparse

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    AssertionExecutor,
    Selector,
    assertion_msg,
    check_for_expected_sections_elements,
    check_for_sections,
    check_if_element_is_not_visible,
    check_if_element_is_visible,
    find_element,
    take_screenshot,
    wait_for_page_load_after_action,
)

NAME = "Advice Article"
SERVICE = "Export Readiness"
TYPE = "article"
URL = None

ARTICLE_NAME = Selector(By.CSS_SELECTOR, "#article h1")
ARTICLE_TEXT = Selector(By.CSS_SELECTOR, ".article-content")
IS_THERE_ANYTHING_WRONG_WITH_THIS_PAGE_LINK = Selector(
    By.CSS_SELECTOR, "section.error-reporting a"
)
SHARE_MENU = Selector(By.CSS_SELECTOR, "ul.sharing-links")
FACEBOOK_BUTTON = Selector(By.ID, "share-facebook")
LINKEDIN_BUTTON = Selector(By.ID, "share-linkedin")
TWITTER_BUTTON = Selector(By.ID, "share-twitter")
EMAIL_BUTTON = Selector(By.ID, "share-email")

SHARE_BUTTONS = {
    "itself": SHARE_MENU,
    "facebook": FACEBOOK_BUTTON,
    "twitter": TWITTER_BUTTON,
    "linkedin": LINKEDIN_BUTTON,
    "email": EMAIL_BUTTON,
}

SELECTORS = {
    "share buttons": SHARE_BUTTONS,
    "breadcrumbs": {
        "itself": Selector(By.CSS_SELECTOR, "nav.breadcrumbs"),
        "links": Selector(By.CSS_SELECTOR, "nav.breadcrumbs a"),
    },
    "article": {
        "article name": ARTICLE_NAME,
        "article text": ARTICLE_TEXT
    },
    "error reporting": {
        "itself": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "report page link": IS_THERE_ANYTHING_WRONG_WITH_THIS_PAGE_LINK,
    },
}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_for_expected_sections_elements(driver, SELECTORS)


def should_see_sections(executor: AssertionExecutor, names: List[str]):
    check_for_sections(executor, all_sections=SELECTORS, sought_sections=names)


def should_not_see_section(driver: WebDriver, name: str):
    section = SELECTORS[name.lower()]
    for key, selector in section.items():
        check_if_element_is_not_visible(driver, selector, element_name=key)


def get_article_name(driver: WebDriver) -> str:
    current_article = find_element(driver, ARTICLE_NAME, element_name="Article name")
    return current_article.text


def should_see_article(driver: WebDriver, name: str):
    current_article = get_article_name(driver)
    with assertion_msg(
        "Expected to see '%s' Article but got '%s'", name, current_article
    ):
        assert current_article.lower() == name.lower()


def go_back_to_article_list(driver: WebDriver):
    element_name = "Go Back link"
    go_back_link = find_element(
        driver, GO_BACK_LINK, element_name=element_name, wait_for_it=False
    )
    check_if_element_is_visible(go_back_link, element_name)
    with wait_for_page_load_after_action(driver):
        go_back_link.click()


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
