# -*- coding: utf-8 -*-
"""Domestic Common Articles Page Object."""
import logging
from typing import List
from urllib import parse as urlparse

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from directory_tests_shared.utils import check_url_path_matches_template
from pages import common_selectors
from pages.common_actions import (
    Selector,
    assertion_msg,
    check_for_sections,
    check_if_element_is_not_visible,
    find_and_click_on_page_element,
    find_element,
    go_to_url,
)
from pages.domestic import actions as domestic_actions

NAME = "Advice article"
SERVICE = Service.DOMESTIC
TYPE = PageType.ARTICLE
URL = URLs.DOMESTIC_ADVICE_ARTICLE.template

ARTICLE_NAME = Selector(By.CSS_SELECTOR, "article h1")
ARTICLE_TEXT = Selector(By.CSS_SELECTOR, ".article-content")
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
        "great.gov.uk": Selector(By.CSS_SELECTOR, ".breadcrumbs a[href='/']"),
        "advice": Selector(
            By.CSS_SELECTOR, "nav.breadcrumbs > ol > li:nth-child(2) > a"
        ),
        "article list": Selector(
            By.CSS_SELECTOR, "nav.breadcrumbs > ol > li:nth-child(3) > a"
        ),
    },
    "article": {"article name": ARTICLE_NAME, "article text": ARTICLE_TEXT},
}
SELECTORS.update(common_selectors.DOMESTIC_HEADER)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.DOMESTIC_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url_path_matches_template(URL, driver.current_url)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def should_not_see_section(driver: WebDriver, name: str):
    section = SELECTORS[name.lower()]
    for key, selector in section.items():
        check_if_element_is_not_visible(driver, selector, element_name=key)


def get_article_name(driver: WebDriver) -> str:
    current_article = find_element(driver, ARTICLE_NAME, element_name="Article name")
    return current_article.text


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


def report_problem(driver: WebDriver):
    find_and_click_on_page_element(
        driver, SELECTORS, "report a problem with the page", wait_for_it=False
    )


def search(driver: WebDriver, phrase: str):
    domestic_actions.search(driver, phrase)
