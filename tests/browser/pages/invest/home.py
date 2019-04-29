# -*- coding: utf-8 -*-
"""Invest in Great Home Page Object."""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType, common_selectors
from pages.common_actions import (
    Selector,
    assertion_msg,
    check_for_sections,
    check_title,
    find_and_click_on_page_element,
    find_element,
    find_elements,
    take_screenshot,
    visit_url,
)
from settings import INVEST_UI_URL

NAME = "Home"
URL = urljoin(INVEST_UI_URL, "")
SERVICE = "Invest"
TYPE = "home"
PAGE_TITLE = "Invest in Great Britain - Home"

TOPIC_LINKS = Selector(
    By.CSS_SELECTOR,
    "section.landing-page-accordions > div > ul > li > a",
    type=ElementType.LINK,
)
TOPIC_CONTENTS = Selector(
    By.CSS_SELECTOR,
    "section.landing-page-accordions > div > ul > li > .accordion-content",
)
SELECTORS = {
    "hero": {"self": Selector(By.CSS_SELECTOR, "#content > section.hero")},
    "reasons to move business to the uk": {
        "self": Selector(By.CSS_SELECTOR, "section.landing-page-accordions"),
        "first": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-accordions > div > ul > li:nth-child(1) > a",
        ),
        "second": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-accordions > div > ul > li:nth-child(2) > a",
        ),
        "third": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-accordions > div > ul > li:nth-child(3) > a",
        ),
    },
    "sectors": {
        "self": Selector(By.CSS_SELECTOR, "section.landing-page-industries"),
        "first": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-industries > div > div > div:nth-child(1) > a",
        ),
        "second": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-industries > div > div > div:nth-child(2) > a",
        ),
        "third": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-industries > div > div > div:nth-child(3) > a",
        ),
        "fourth": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-industries > div > div > div:nth-child(4) > a",
        ),
        "fifth": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-industries > div > div > div:nth-child(5) > a",
        ),
        "sixth": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-industries > div > div > div:nth-child(6) > a",
        ),
        "see more industries": Selector(
            By.CSS_SELECTOR, "section.landing-page-industries > div > a"
        ),
    },
    "setup guides": {
        "self": Selector(By.CSS_SELECTOR, "section.landing-page-setup-guide"),
        "first": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-setup-guide div.card-grid > div:nth-child(1) a h3",
        ),
        "second": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-setup-guide div.card-grid > div:nth-child(2) a h3",
        ),
        "third": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-setup-guide div.card-grid > div:nth-child(3) a h3",
        ),
        "fourth": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-setup-guide div.card-grid > div:nth-child(4) a h3",
        ),
        "fifth": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-setup-guide div.card-grid > div:nth-child(5) a h3",
        ),
        "sixth": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-setup-guide div.card-grid > div:nth-child(6) a h3",
        ),
    },
    "how we help": {
        "self": Selector(By.CSS_SELECTOR, "section.landing-page-how-we-help")
    },
    "build connections": {
        "build connections - icon": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-how-we-help ul > li:nth-child(1) > div > img",
        ),
        "build connections - text": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-how-we-help ul > li:nth-child(1) > div > p",
        ),
    },
    "apply for visas": {
        "apply for visas - icon": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-how-we-help ul > li:nth-child(2) > div > img",
        ),
        "apply for visas - text": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-how-we-help ul > li:nth-child(2) > div > p",
        ),
    },
    "find grants": {
        "find grants - icon": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-how-we-help ul > li:nth-child(3) > div > img",
        ),
        "find grants - text": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-how-we-help ul > li:nth-child(3) > div > p",
        ),
    },
    "get insights": {
        "get insights - icon": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-how-we-help ul > li:nth-child(4) > div > img",
        ),
        "get insights - text": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-how-we-help ul > li:nth-child(4) > div > p",
        ),
    },
    "grow workforce": {
        "grow workforce - icon": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-how-we-help ul > li:nth-child(5) > div > img",
        ),
        "grow workforce - text": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-how-we-help ul > li:nth-child(5) > div > p",
        ),
    },
    "contact us for help": {
        "contact us for help - link": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-how-we-help ul > li:nth-child(6) > div > a",
        ),
        "contact us for help - text": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-how-we-help ul > li:nth-child(6) > div > p",
        ),
    },
}
SELECTORS.update(common_selectors.HEADER_INVEST)
SELECTORS.update(common_selectors.BETA_BAR)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.FOOTER_INVEST)


def visit(driver: WebDriver):
    visit_url(driver, URL)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, PAGE_TITLE)
    check_title(driver, PAGE_TITLE, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def open_link(driver: WebDriver, name: str):
    driver.find_element_by_link_text(name).click()


def open_all_topics(driver: WebDriver):
    topic_links = find_elements(driver, TOPIC_LINKS)
    for link in topic_links:
        link.click()


def should_see_all_topics(driver: WebDriver):
    contents = find_elements(driver, TOPIC_CONTENTS)
    for content in contents:
        with assertion_msg("Can't see contents for: {}".format(content.text)):
            assert content.is_displayed()


def clean_name(name: str) -> str:
    return name.split(" - ")[1].strip()


def open_industry(driver: WebDriver, industry_name: str):
    industry_name = clean_name(industry_name)
    selector = Selector(By.PARTIAL_LINK_TEXT, industry_name)
    logging.debug("Looking for: {}".format(industry_name))
    industry_link = find_element(
        driver, selector, element_name="Industry card", wait_for_it=False
    )
    industry_link.click()
    take_screenshot(driver, PAGE_TITLE + " after opening " + industry_name)


def open_guide(driver: WebDriver, guide_name: str):
    guide_name = clean_name(guide_name)
    selector = Selector(By.PARTIAL_LINK_TEXT, guide_name)
    logging.debug("Looking for: {}".format(guide_name))
    guide = find_element(driver, selector, element_name="Guide card", wait_for_it=False)
    guide.click()
    take_screenshot(driver, PAGE_TITLE + " after opening " + guide_name)


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, PAGE_TITLE + " after clicking on " + element_name)


def see_more_industries(driver: WebDriver):
    click_on_page_element(driver, "see more industries")
