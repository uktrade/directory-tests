# -*- coding: utf-8 -*-
"""Invest in Great Home Page Object."""
import logging
from enum import Enum
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

NAME = "UK Setup guide"
SERVICE = "invest"
TYPE = "guide"
URL = urljoin(INVEST_UI_URL, "uk-setup-guide/")
BASE_URL = urljoin(INVEST_UI_URL, "uk-setup-guide/")
PAGE_TITLE = "Invest in Great Britain -"


class URLS(Enum):
    """Lists all URLs for guide pages."""

    UK_SETUP = urljoin(BASE_URL, "")
    APPLY_FOR_A_UK_VISA = urljoin(BASE_URL, "apply-for-a-uk-visa/")
    ESTABLISH_A_BASE_FOR_BUSINESS_IN_THE_UK = urljoin(
        BASE_URL, "establish-a-base-for-business-in-the-uk/"
    )
    HIRE_SKILLED_WORKERS_FOR_YOUR_UK_OPERATIONS = urljoin(
        BASE_URL, "hire-skilled-workers-for-your-uk-operations/"
    )
    OPEN_A_UK_BUSINESS_BANK_ACCOUNT = urljoin(
        BASE_URL, "open-a-uk-business-bank-account/"
    )
    SET_UP_A_COMPANY_IN_THE_UK = urljoin(BASE_URL, "set-up-a-company-in-the-uk/")
    UNDERSTAND_THE_UKS_TAX_INCENTIVES_AND_LEGAL_FRAMEWORK = urljoin(
        BASE_URL, "understand-uk-tax-and-incentives/"
    )


SELECTORS = {
    "header": {
        "self": Selector(By.ID, "invest-header"),
        "logo": Selector(By.CSS_SELECTOR, "#invest-header > div.header-bar  a"),
    },
    "beta bar": {
        "self": Selector(By.ID, "header-beta-bar"),
        "beta bar": Selector(By.CSS_SELECTOR, "#header-beta-bar strong"),
        "feedback link": Selector(By.CSS_SELECTOR, "#header-beta-bar a"),
    },
    "hero": {"self": Selector(By.CSS_SELECTOR, "#content > section.hero")},
    "industry accordions": {
        "self": Selector(By.CSS_SELECTOR, "section.industry-page-accordions"),
        "accordion expanders": Selector(
            By.CSS_SELECTOR, "section.industry-page-accordions a.accordion-expander"
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


def visit(executor: Executor, *, first_time: bool = False, page_name: str = None):
    if page_name:
        enum_key = (
            page_name.lower()
            .replace("invest - ", "")
            .replace("industry", "")
            .replace("guide", "")
            .strip()
            .replace(" ", "_")
            .replace("-", "_")
            .replace("'", "")
            .replace(",", "")
            .upper()
        )
        url = URLS[enum_key].value
    else:
        url = URL
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


def clean_name(name: str) -> str:
    return (
        name.replace("Invest - ", "")
        .replace("industry", "")
        .replace("guide", "")
        .strip()
    )


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
