# -*- coding: utf-8 -*-
"""UK Setup Guide - landing page."""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import common_selectors
from pages.common_actions import (
    Selector,
    check_for_sections,
    check_url,
    find_and_click_on_page_element,
    find_element,
    take_screenshot,
    visit_url,
)
from settings import INVEST_UI_URL

NAME = "UK Setup guide"
SERVICE = "invest"
TYPE = "landing"
URL = urljoin(INVEST_UI_URL, "uk-setup-guide/")
PAGE_TITLE = "Invest In Great Britain - UK Setup Guide"


SELECTORS = {
    "hero": {"self": Selector(By.CSS_SELECTOR, "#content > section.hero")},
    "introduction": {
        "self": Selector(By.CSS_SELECTOR, "#content section.setup-guide .intro"),
        "header": Selector(By.CSS_SELECTOR, "#content section.setup-guide .intro h2"),
        "paragraph": Selector(By.CSS_SELECTOR, "#content section.setup-guide .intro p"),
    },
    "guides": {
        "self": Selector(
            By.CSS_SELECTOR, "#content > section.setup-guide > div:nth-child(2)"
        ),
        "cards": Selector(By.CSS_SELECTOR, "#content > section.setup-guide div.card"),
        "Apply for a UK visa": Selector(
            By.CSS_SELECTOR, "div.card a[href='apply-uk-visa']"
        ),
        "Establish a base for business in the UK": Selector(
            By.CSS_SELECTOR, "div.card a[href='establish-base-business-uk']"
        ),
        "Hire skilled workers for your UK operations": Selector(
            By.CSS_SELECTOR,
            "div.card a[href='hire-skilled-workers-your-uk-operations']",
        ),
        "Open a UK business bank account": Selector(
            By.CSS_SELECTOR, "div.card a[href='open-uk-business-bank-account']"
        ),
        "Set up a company in the UK": Selector(
            By.CSS_SELECTOR, "div.card a[href='setup-your-business-uk']"
        ),
        "Understand the UK's tax, incentives and legal framework": Selector(
            By.CSS_SELECTOR, "div.card a[href='understand-uk-tax-and-incentives']"
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
    check_url(driver, URL, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def open_link(driver: WebDriver, name: str):
    driver.find_element_by_link_text(name).click()


def open_guide(driver: WebDriver, guide_name: str):
    guide_name = guide_name.split(" - ")[1].strip()
    selector = Selector(By.PARTIAL_LINK_TEXT, guide_name)
    logging.debug("Looking for: {}".format(guide_name))
    guide = find_element(driver, selector, element_name="Guide card", wait_for_it=False)
    guide.click()
    take_screenshot(driver, PAGE_TITLE + " after opening " + guide_name)


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, PAGE_TITLE + " after clicking on " + element_name)
