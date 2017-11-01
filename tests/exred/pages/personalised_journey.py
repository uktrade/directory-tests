# -*- coding: utf-8 -*-
"""ExRed Personalised Journey - Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from settings import EXRED_UI_URL
from utils import assertion_msg, selenium_action, take_screenshot

NAME = "ExRed Personalised Journey"
URL = urljoin(EXRED_UI_URL, "custom")

SHOW_MORE_BUTTON = "#persona-overview a.button.more"
HERO_SECTION = {
    "hero - title": "section.hero-section h1",
    "hero - introduction": "section.hero-section p",
    "hero - exporting is great logo": "section.hero-section img",
}
FACTS_SECTION = {
    "facts - intro": "#content > section.sector-fact p.intro",
    "facts - figures": "#content > section.sector-fact p.figure",
}
ARTICLES_SECTION = {
    "articles - heading": "#persona-overview h2",
    "articles - introduction": "#persona-overview p.intro",
    "articles - article list": "#persona-overview div.section-content-list",
}
TOP_10_SECTION = {
    "top 10 - heading": "#content > section.markets h1",
    "top 10 - table": "#content > section.markets table",
}
SERVICES_SECTION = {
    "services - heading": "section.service-section h2",
    "services - intro": "section.service-section .intro",
    "services - other": "#other-services > div > div",
}
GUIDANCE_SECTION = {
    "guidance - heading": "#resource-guidance h2",
    "guidance - introduction": "#resource-guidance p.section-intro",
    "guidance - categories": "#resource-guidance div.group",
}

EXPECTED_ELEMENTS = {}
EXPECTED_ELEMENTS.update(HERO_SECTION)
SHOW_MORE_BUTTON = "#js-paginate-list-more"


def should_be_here(driver: webdriver):
    for element_name, element_selector in EXPECTED_ELEMENTS.items():
        with selenium_action(
                driver, "Could not find '%s' using '%s'", element_name,
                element_selector):
            element = driver.find_element_by_css_selector(element_selector)
        with assertion_msg(
                "It looks like '%s' element is not visible on %s",
                element_name, NAME):
            assert element.is_displayed()
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def show_more(driver: webdriver):
    with selenium_action(
            driver, "Could not find 'Show More' button using '%s'",
            SHOW_MORE_BUTTON):
        button = driver.find_element_by_css_selector(SHOW_MORE_BUTTON)
        assert button.is_displayed()
    button.click()
    take_screenshot(driver, NAME + " after showing more")


def show_all_articles(driver: webdriver):
    with selenium_action(
            driver, "Could not find 'Show More' button using '%s'",
            SHOW_MORE_BUTTON):
        button = driver.find_element_by_css_selector(SHOW_MORE_BUTTON)
    while button.is_displayed():
        button.click()
    take_screenshot(driver, NAME + " after showing all articles")
