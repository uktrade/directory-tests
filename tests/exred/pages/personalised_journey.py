# -*- coding: utf-8 -*-
"""ExRed Personalised Journey - Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

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
TOP_IMPORTER = "#top_importer_name"
TRADE_VALUE = "#top_importer_global_trade_value"
TOP_10_TRADE_VALUE = ".cell-global_trade_value"
SECTIONS = {
    "hero": {
        "title": "section.hero-section h1",
        "introduction": "section.hero-section p",
        "exporting is great logo": "section.hero-section img",
        "update preferences link": "section.hero-section a.preferences",
    },
    "facts": {
        "intro": "#content > section.sector-fact p.intro",
        "figures": "#content > section.sector-fact p.figure",
    },
    "articles": {
        "heading": "#persona-overview h2",
        "introduction": "#persona-overview p.intro",
        "article list": "#persona-overview div.section-content-list",
    },
    "top 10": {
        "heading": "section.top-markets h2",
        "intro": "section.top-markets .intro",
        "table": "#top-of-the-markets",
        "source data": "section.top-markets #market-source-data",
    },
    "services": {
        "heading": "section.service-section h2",
        "intro": "section.service-section .intro",
        "other": "#other-services > div > div",
    },
    "fas section": {
        "heading": "section.service-section.fas h2",
        "fas image": "section.service-section.fas img",
        "intro": "section.service-section.fas .intro",
        "create a trade profile": "section.service-section.fas .intro .button",
    },
    "exopps tile": {
        "heading": "#other-services div.lg-2:nth-child(2) h3",
        "soo image": "#other-services div.lg-2:nth-child(2) img",
        "intro": "#other-services div.lg-2:nth-child(2) p",
        "find marketplaces link": "#other-services div.lg-2:nth-child(2) a",
    },
    "exopps section": {
        "heading": "section.service-section.soo h2",
        "soo image": "section.service-section.soo img",
        "intro": "section.service-section.soo .intro",
        "find marketplaces button": "section.service-section.soo .intro .button",
    },
    "soo section": {
        "heading": "section.service-section.soo h2",
        "soo image": "section.service-section.soo img",
        "intro": "section.service-section.soo .intro",
        "find marketplaces button": "section.service-section.soo .intro .button",
    },
    "soo tile": {
        "heading": "#other-services div.lg-2:nth-child(1) h3",
        "soo image": "#other-services div.lg-2:nth-child(1) img",
        "intro": "#other-services div.lg-2:nth-child(1) p",
        "find marketplaces link": "#other-services div.lg-2:nth-child(1) a",
    },
    "article list": {
        "itself": "#articles",
        "heading": "#articles h2",
        "introduction": "#articles .intro",
        "article list": "#articles .section-content-list",
    },
    "guidance": {
        "itself": "#resource-guidance",
        "guidance - heading": "#resource-guidance h2.section-header",
        "guidance - introduction": "#resource-guidance p.intro",
        "guidance - categories": "#resource-guidance .group",
        "market research": MARKET_RESEARCH_LINK,
        "customer insight": CUSTOMER_INSIGHT_LINK,
        "finance": FINANCE_LINK,
        "business planning": BUSINESS_LINK,
        "getting paid": GETTING_PAID_LINK,
        "operations and compliance": OPERATIONS_AND_COMPLIANCE_LINK,
    },
    "case studies": {
        "heading": "#carousel h2",
        "intro": "#carousel .intro",
        "article": "#carousel .ed-carousel-container",
        "previous article": "#carousel label.ed-carousel__control--backward",
        "next article": "#carousel label.ed-carousel__control--forward",
        "case study head link": ".ed-carousel__track > div:nth-child(1) h3 a",
        "case study intro": ".ed-carousel__track > div:nth-child(1) p",
        "case study intro link": ".ed-carousel__track > div:nth-child(1) div > a",
        "carousel indicator #1": "#carousel .ed-carousel__indicator[for='1']",
        "carousel indicator #2": "#carousel .ed-carousel__indicator[for='2']",
        "carousel indicator #3": "#carousel .ed-carousel__indicator[for='3']",
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


def open(driver: webdriver, group: str, element: str):
    link = SECTIONS[group.lower()][element.lower()]
    button = driver.find_element_by_css_selector(link)
    assert button.is_displayed()
    button.click()
    take_screenshot(
        driver, NAME + " after clicking on: %s link".format(element))


def should_see_section(driver: webdriver, name: str):
    section = SECTIONS[name]
    for key, selector in section.items():
        with selenium_action(
                driver, "Could not find: '%s' element in '%s' section using "
                        "'%s' selector",
                key, name, selector):
            element = driver.find_element_by_css_selector(selector)
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
        with assertion_msg(
                "'%s' in '%s' is not displayed", key, name):
            assert element.is_displayed()


def check_top_facts_values(driver: webdriver):
    top_importer = driver.find_element_by_css_selector(TOP_IMPORTER).text
    trade_value = driver.find_element_by_css_selector(TRADE_VALUE).text

    try:
        tr = driver.find_element_by_css_selector(
            "#row-{}".format(top_importer))
        cell = tr.find_element_by_css_selector(TOP_10_TRADE_VALUE).text
        with assertion_msg(
                "Expected to see 'Export value from the world' for %s to be %s"
                " but got %s", top_importer, trade_value, cell):
            assert cell == trade_value
    except NoSuchElementException:
        logging.debug(
            "Country mentioned in Top Facts: %s is not present in the Top 10 "
            "Importers table. Won't check the the trade value")


def check_facts_and_top_10(driver: webdriver, sector_code: str):
    """There are no Facts & Top 10 data for Service Sectors (start with EB)."""
    if sector_code.startswith("EB"):
        logging.debug(
            "Exported chose service sector: %s for which there are no facts "
            "and information on top 10 importers", sector_code)
    else:
        should_see_section(driver, "facts")
        should_see_section(driver, "top 10")
        check_top_facts_values(driver)
