# -*- coding: utf-8 -*-
"""UK Setup Guide Pages."""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    AssertionExecutor,
    Executor,
    Selector,
    assertion_msg,
    check_for_sections,
    check_url,
    find_and_click_on_page_element,
    take_screenshot,
    visit_url,
)
from settings import INVEST_UI_URL

NAME = "Guide"
NAMES = [
    "Apply for a UK visa",
    "Establish a base for business in the UK",
    "Hire skilled workers for your UK operations",
    "Open a UK business bank account",
    "Register a company in the UK",
    "Understand UK tax and incentives",
]
SERVICE = "invest"
TYPE = "guide"
URL = urljoin(INVEST_UI_URL, "uk-setup-guide/")
PAGE_TITLE = "Invest in Great Britain -"

SELECTORS = {
    "header": {
        "self": Selector(By.ID, "invest-header"),
        "logo": Selector(By.CSS_SELECTOR, "#invest-header > div.header-bar a"),
        "contact us": Selector(
            By.CSS_SELECTOR, "#invest-header a[href='/contact/']"
        ),
    },
    "beta bar": {
        "self": Selector(By.ID, "header-beta-bar"),
        "beta bar": Selector(By.CSS_SELECTOR, "#header-beta-bar strong"),
        "feedback": Selector(By.CSS_SELECTOR, "#header-beta-bar a"),
    },
    "hero": {"self": Selector(By.CSS_SELECTOR, "#content > section.hero")},
    "content": {
        "self": Selector(By.CSS_SELECTOR, "section.setup-guide"),
        "accordion expanders": Selector(
            By.CSS_SELECTOR, "section.setup-guide a.accordion-expander"
        ),
    },
    "report this page": {
        "self": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "report link": Selector(By.CSS_SELECTOR, "section.error-reporting a"),
    },
    "footer": {
        "self": Selector(By.ID, "invest-footer"),
        "uk gov logo": Selector(
            By.CSS_SELECTOR,
            "#invest-footer div.footer-branding > img:nth-child(1)",
        ),
        "invest logo": Selector(
            By.CSS_SELECTOR,
            "#invest-footer div.footer-branding > img:nth-child(2)",
        ),
    },
}

URLs = {
    "apply for a uk visa": urljoin(URL, "apply-uk-visa/"),
    "establish a base for business in the uk": urljoin(
        URL, "establish-base-business-uk/"
    ),
    "hire skilled workers for your uk operations": urljoin(
        URL, "hire-skilled-workers-your-uk-operations/"
    ),
    "open a uk business bank account": urljoin(
        URL, "open-uk-business-bank-account/"
    ),
    "register a company in the uk": urljoin(URL, "setup-your-business-uk/"),
    "understand uk tax and incentives": urljoin(
        URL, "understand-uk-tax-and-incentives/"
    ),
}


def clean_name(name: str) -> str:
    return name.split(" - ")[1].strip()


def visit(
    executor: Executor, *, page_name: str = None):
    url = URLs[clean_name(page_name).lower()]
    visit_url(executor, url)


def should_be_here(executor: Executor, *, page_name: str):
    take_screenshot(executor, PAGE_TITLE)
    check_url(executor, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)


def should_see_sections(executor: AssertionExecutor, names: List[str]):
    check_for_sections(executor, all_sections=SELECTORS, sought_sections=names)


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
