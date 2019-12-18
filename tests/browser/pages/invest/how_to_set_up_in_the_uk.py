# -*- coding: utf-8 -*-
"""UK Setup Guide - landing page."""
import logging
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import common_selectors
from pages.common_actions import (
    Selector,
    check_for_sections,
    check_url,
    find_element,
    go_to_url,
    take_screenshot,
)

NAME = "How to set up in the UK"
SERVICE = Service.INVEST
TYPE = PageType.LANDING
URL = URLs.INVEST_UK_SETUP_GUIDE.absolute
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
SELECTORS.update(common_selectors.INVEST_HEADER)
SELECTORS.update(common_selectors.BETA_BAR)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.INVEST_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def open_guide(driver: WebDriver, guide_name: str):
    guide_name = guide_name.split(" - ")[1].strip()
    selector = Selector(By.PARTIAL_LINK_TEXT, guide_name)
    logging.debug("Looking for: {}".format(guide_name))
    guide = find_element(driver, selector, element_name="Guide card", wait_for_it=False)
    guide.click()
    take_screenshot(driver, PAGE_TITLE + " after opening " + guide_name)
