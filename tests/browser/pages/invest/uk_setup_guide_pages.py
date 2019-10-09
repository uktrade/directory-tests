# -*- coding: utf-8 -*-
"""UK Setup Guide Pages."""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import Service
from directory_tests_shared.settings import INTERNATIONAL_URL
from pages import common_selectors
from pages.common_actions import (
    Selector,
    assertion_msg,
    check_for_sections,
    check_url,
    find_and_click_on_page_element,
    take_screenshot,
    visit_url,
)

NAME = "How to set up in the UK"
NAMES = [
    "Access finance in the UK",
    "Access finance in the UK (Staging)",
    "DIT's guide to UK Capital Gains Tax",
    "DIT's guide to UK Corporation Tax",
    "DIT's Guide to UK Venture Capital Schemes",
    "Establish a UK business base",
    "Open a UK business bank account",
    "Open a UK business bank account (Staging)",
    "Register a company in the UK",
    "UK Income Tax",
    "UK infrastructure",
    "UK talent and labour",
    "UK tax and incentives",
    "UK tax and incentives (Staging)",
]
SERVICE = Service.INVEST
TYPE = "guide"
URL = URLs.INVEST_UK_SETUP_GUIDE.absolute
URL_STAGING = urljoin(INTERNATIONAL_URL, "content/how-to-setup-in-the-uk/")
PAGE_TITLE = "Invest in Great Britain -"

SELECTORS = {
    "hero": {"self": Selector(By.CSS_SELECTOR, "#content > section.hero")},
    "content": {
        "self": Selector(By.CSS_SELECTOR, "section.setup-guide"),
        "accordion expanders": Selector(
            By.CSS_SELECTOR, "section.setup-guide a.accordion-expander"
        ),
    },
}
SELECTORS.update(common_selectors.INVEST_HEADER)
SELECTORS.update(common_selectors.BETA_BAR)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.INVEST_FOOTER)

SubURLs = {
    # Dev & UAT
    "access finance in the uk": URLs.INVEST_UK_SETUP_GUIDE_ACCESS_FINANCE.absolute,
    "dit's guide to uk capital gains tax": URLs.INVEST_UK_SETUP_GUIDE_DIT_CAPITAL_GAINS.absolute,
    "dit's guide to uk corporation tax": URLs.INVEST_UK_SETUP_GUIDE_DIT_CORPORATION_TAX.absolute,
    "dit's guide to uk venture capital schemes": URLs.INVEST_UK_SETUP_GUIDE_DIT_VENTURE_CAPITAL.absolute,
    "establish a uk business base": URLs.INVEST_UK_SETUP_GUIDE_ESTABLISH_A_BASE.absolute,
    "register a company in the uk": URLs.INVEST_UK_SETUP_GUIDE_REGISTER_A_COMPANY.absolute,
    "uk income tax": URLs.INVEST_UK_SETUP_GUIDE_UK_INCOME_TAX.absolute,
    "uk infrastructure": URLs.INVEST_UK_SETUP_GUIDE_UK_INFRASTRUCTURE.absolute,
    "uk talent and labour": URLs.INVEST_UK_SETUP_GUIDE_HIRE_SKILLED_WORKERS.absolute,
    "uk tax and incentives": URLs.INVEST_UK_SETUP_GUIDE_UK_TAX.absolute,
    # Staging
    "access finance in the uk (staging)": urljoin(
        URL_STAGING, "access-finance-in-the-uk/"
    ),
    "open a uk business bank account (staging)": urljoin(
        URL_STAGING, "open-a-uk-business-bank-account/"
    ),
    "uk tax and incentives (staging)": urljoin(URL_STAGING, "uk-tax-and-incentives/"),
}


def clean_name(name: str) -> str:
    return name.split(" - ")[1].strip()


def visit(driver: WebDriver, *, page_name: str = None):
    url = SubURLs[page_name] if page_name else URL
    visit_url(driver, url)


def should_be_here(driver: WebDriver, *, page_name: str):
    take_screenshot(driver, PAGE_TITLE)
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def open_link(driver: WebDriver, name: str):
    driver.find_element_by_link_text(name).click()


def should_see_content_for(driver: WebDriver, guide_name: str):
    source = driver.page_source
    guide_name = clean_name(guide_name)
    logging.debug("Looking for: {}".format(guide_name))
    with assertion_msg(
        "Expected to find term '%s' in the source of the page %s",
        guide_name,
        driver.current_url,
    ):
        assert guide_name.lower() in source.lower()


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, PAGE_TITLE + " after clicking on " + element_name)
