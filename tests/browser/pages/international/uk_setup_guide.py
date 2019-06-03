# -*- coding: utf-8 -*-
"""International - UK setup guide"""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.remote.webdriver import WebDriver

from pages import common_selectors
from pages.common_actions import (
    check_for_sections,
    check_url,
    take_screenshot,
    visit_url,
)
from settings import EXRED_UI_URL

NAME = "UK setup guide"
NAMES = [
    "Access finance in the UK",
    "Establish a UK business base",
    "Hire skilled workers for your UK operations",
    "Open a UK business bank account",
    "Register a company in the UK",
    "Research and development (R&D) support in the UK",
    "UK tax and incentives",
    "UK visas and migration",
]
SERVICE = "International"
TYPE = "uk setup guide"
URL = urljoin(EXRED_UI_URL, "international/content/how-to-setup-in-the-uk/")
PAGE_TITLE = " - great.gov.uk International"


URLs = {
    "Access finance in the UK": urljoin(URL, "access-finance-in-the-uk/"),
    "Establish a UK business base": urljoin(URL, "establish-a-base-for-business-in-the-uk/"),
    "Hire skilled workers for your UK operations": urljoin(URL, "hire-skilled-workers-for-your-uk-operations/"),
    "Open a UK business bank account": urljoin(URL, "open-a-uk-business-bank-account/"),
    "Register a company in the UK": urljoin(URL, "register-a-company-in-the-uk/"),
    "Research and development (R&D) support in the UK": urljoin(URL, "research-and-development-rd-support-in-the-uk/"),
    "UK tax and incentives": urljoin(URL, "uk-tax-and-incentives/"),
    "UK visas and migration": urljoin(URL, "uk-visas-and-migration/"),
}


SELECTORS = {
}
SELECTORS.update(common_selectors.HEADER_INTERNATIONAL)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.FOOTER_INTERNATIONAL)


def visit(driver: WebDriver, *, page_name: str = None):
    url = URLs[page_name.split(" - ")[1]] if page_name else URL
    visit_url(driver, url)


def should_be_here(driver: WebDriver, *, page_name: str):
    take_screenshot(driver, PAGE_TITLE)
    url = URLs[page_name.lower()] if page_name else URL
    check_url(driver, url, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)