# -*- coding: utf-8 -*-
"""ExRed - Services page"""
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Selector,
    check_for_sections,
    take_screenshot,
    check_url,
    go_to_url
)
from settings import EXRED_UI_URL

NAME = "Services"
SERVICE = "Export Readiness"
TYPE = "services list"
URL = urljoin(EXRED_UI_URL, "services/")

SELECTORS = {
    "breadcrumbs": {
        "itself": Selector(By.CSS_SELECTOR, "div.breadcrumbs"),
        "current page": Selector(
            By.CSS_SELECTOR, "div.breadcrumbs li[aria-current='page']"
        ),
        "links": Selector(By.CSS_SELECTOR, "div.breadcrumbs a"),
    },
    "services": {
        "itself": Selector(By.ID, "services"),
        "heading": Selector(By.ID, "services-section-title"),
        "description": Selector(By.ID, "services-section-description"),
        "service cards": Selector(By.CSS_SELECTOR, "#services .card"),
        "create a business profile": Selector(By.ID, "find-a-buyer-link", type=ElementType.LINK),
        "find online marketplaces": Selector(By.ID, "selling-online-overseas-link", type=ElementType.LINK),
        "find export opportunities": Selector(By.ID, "export-opportunities-link", type=ElementType.LINK),
        "uk export finance": Selector(By.ID, "uk-export-finance-link", type=ElementType.LINK),
        "find events and visits": Selector(By.ID, "events-link", type=ElementType.LINK),
        "get an eori number": Selector(By.ID, "govuk-eori-link", type=ElementType.LINK),
    },
    "error reporting": {
        "itself": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "link": Selector(By.ID, "error-reporting-section-contact-us"),
    },
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)
