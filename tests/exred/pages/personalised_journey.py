# -*- coding: utf-8 -*-
"""ExRed Personalised Journey - Page Object."""
import logging

from selenium import webdriver
from selenium.webdriver import ActionChains

from utils import assertion_msg, get_absolute_url, take_screenshot

NAME = "ExRed Personalised Journey"
URL = get_absolute_url(NAME)

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
# ARTICLES_SECTION is not included as it's not displayed to Regular Exporters
EXPECTED_ELEMENTS.update(HERO_SECTION)
# EXPECTED_ELEMENTS.update(FACTS_SECTION)
# EXPECTED_ELEMENTS.update(TOP_10_SECTION)
EXPECTED_ELEMENTS.update(SERVICES_SECTION)
EXPECTED_ELEMENTS.update(GUIDANCE_SECTION)


def should_be_here(driver: webdriver):
    for element_name, element_selector in EXPECTED_ELEMENTS.items():
        element = driver.find_element_by_css_selector(element_selector)
        with assertion_msg(
                "It looks like '%s' element is not visible on %s",
                element_name, NAME):
            assert element.is_displayed()
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def show_more(driver: webdriver):
    button = driver.find_element_by_css_selector(SHOW_MORE_BUTTON)
    assert button.is_displayed()
    actions = ActionChains(driver)
    actions.move_to_element(button)
    actions.click(button)
    actions.perform()
    take_screenshot(driver, NAME + " after showing more")
