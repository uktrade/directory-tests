# -*- coding: utf-8 -*-
"""ExRed Personalised Journey - Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from registry.articles import get_articles
from settings import EXRED_UI_URL
from utils import assertion_msg, selenium_action, take_screenshot

NAME = "ExRed Personalised Journey"
URL = urljoin(EXRED_UI_URL, "custom")

SHOW_MORE_BUTTON = "#js-paginate-list-more"
READ_COUNTER = "#articles .scope-indicator .position > span.from"

MARKET_RESEARCH_LINK = "#resource-guidance a[href='/market-research']"
CUSTOMER_INSIGHT_LINK = "#resource-guidance a[href='/customer-insight']"
FINANCE_LINK = "#resource-guidance a[href='/finance']"
BUSINESS_LINK = "#resource-guidance a[href='/business-planning']"
GETTING_PAID_LINK = "#resource-guidance a[href='/getting-paid']"
OPERATIONS_AND_COMPLIANCE_LINK = "#resource-guidance a[href='/operations-and-compliance']"

SECTIONS = {
    "hero": {
        "hero - title": "section.hero-section h1",
        "hero - introduction": "section.hero-section p",
        "hero - exporting is great logo": "section.hero-section img",
    },
    "facts": {
        "facts - intro": "#content > section.sector-fact p.intro",
        "facts - figures": "#content > section.sector-fact p.figure",
    },
    "articles": {
        "articles - heading": "#persona-overview h2",
        "articles - introduction": "#persona-overview p.intro",
        "articles - article list": "#persona-overview div.section-content-list",
    },
    "top 10": {
        "top 10 - heading": "#content > section.markets h1",
        "top 10 - table": "#content > section.markets table",
    },
    "services": {
        "services - heading": "section.service-section h2",
        "services - intro": "section.service-section .intro",
        "services - other": "#other-services > div > div",
    },
    "guidance": {
        "guidance - heading": "#resource-guidance h2",
        "guidance - introduction": "#resource-guidance p.section-intro",
        "guidance - categories": "#resource-guidance div.group",
        "market research": MARKET_RESEARCH_LINK,
        "customer insight": CUSTOMER_INSIGHT_LINK,
        "finance": FINANCE_LINK,
        "business planning": BUSINESS_LINK,
        "getting paid": GETTING_PAID_LINK,
        "operations and compliance": OPERATIONS_AND_COMPLIANCE_LINK,
    }
}


def should_be_here(driver: webdriver):
    for element_name, element_selector in SECTIONS["hero"].items():
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


def should_see_read_counter(driver: webdriver, *, exporter_status: str = None):
    show_all_articles(driver)
    with selenium_action(
            driver, "Could not find 'Show More' button using '%s'",
            SHOW_MORE_BUTTON):
        counter = driver.find_element_by_css_selector(READ_COUNTER)
    with assertion_msg(
            "Guidance Article Read Counter is not visible on '%s' page", NAME):
        assert counter.is_displayed()
    if exporter_status:
        expected_number_articles = len(get_articles(
            group="personalised journey", category=exporter_status.lower()))
        given_number_articles = int(counter.text)
        with assertion_msg(
                "Expected the Article Read Counter to be: %d but got %d",
                expected_number_articles, given_number_articles):
            assert given_number_articles == expected_number_articles
