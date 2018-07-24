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
    check_title,
    check_url,
    take_screenshot,
    visit_url,
)
from settings import INVEST_UI_URL

NAME = "Guide"
NAMES = [
    "Apply for a UK visa guide",
    "Establish a base for business in the UK guide",
    "Hire skilled workers for your UK operations guide",
    "Open a UK business bank account guide",
    "Set up a company in the UK guide",
    "Understand the UK's tax, incentives and legal framework guide",
]
SERVICE = "invest"
TYPE = "guide"
URL = urljoin(INVEST_UI_URL, "uk-setup-guide/")
PAGE_TITLE = "Invest in Great Britain -"

SELECTORS = {
    "header": {
        "self": Selector(By.ID, "invest-header"),
        "logo": Selector(By.CSS_SELECTOR, "#invest-header > div.header-bar a"),
    },
    "beta bar": {
        "self": Selector(By.ID, "header-beta-bar"),
        "beta bar": Selector(By.CSS_SELECTOR, "#header-beta-bar strong"),
        "feedback link": Selector(By.CSS_SELECTOR, "#header-beta-bar a"),
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
            By.CSS_SELECTOR, "#invest-footer div.footer-branding > img:nth-child(1)"
        ),
        "invest logo": Selector(
            By.CSS_SELECTOR, "#invest-footer div.footer-branding > img:nth-child(2)"
        ),
    },
}

URLs = {
    "apply for a uk visa": urljoin(URL, "apply-for-a-uk-visa/"),
    "establish a base for business in the uk": urljoin(
        URL, "establish-a-base-for-business-in-the-uk/"
    ),
    "hire skilled workers for your uk operations": urljoin(
        URL, "hire-skilled-workers-for-your-uk-operations/"
    ),
    "open a uk business bank account": urljoin(URL, "open-a-uk-business-bank-account/"),
    "set up a company in the uk": urljoin(URL, "set-up-a-company-in-the-uk/"),
    "understand the uk's tax, incentives and legal framework": urljoin(
        URL, "understand-uk-tax-and-incentives/"
    ),
}


def clean_name(name: str) -> str:
    return (
        name.lower()
        .replace("invest - ", "")
        .replace("industry", "")
        .replace("guide", "")
        .strip()
    )


def visit(executor: Executor, *, page_name: str = None, first_time: bool = False):
    url = URLs[clean_name(page_name)]
    visit_url(executor, url)


def should_be_here(executor: Executor):
    check_title(executor, PAGE_TITLE, exact_match=False)
    check_url(executor, URL, exact_match=False)
    take_screenshot(executor, PAGE_TITLE)
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
