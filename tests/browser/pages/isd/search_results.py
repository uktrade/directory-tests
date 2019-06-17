# -*- coding: utf-8 -*-
"""Find a Supplier - ISD Search Results Page Object."""
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
    take_screenshot,
)
from settings import EXRED_UI_URL

NAME = "Search results"
SERVICE = "ISD"
TYPE = "search results"
URL = urljoin(EXRED_UI_URL, "investment-support-directory/search/?")
PAGE_TITLE = "Find a UK specialist"

SELECTORS = {
    "results summary": {
        "number of results": Selector(
            By.CSS_SELECTOR, "#hero-container > div > div > div.column-two-thirds > h2"
        )
    },
    "search form": {
        "itself": Selector(By.ID, "-container"),
        "search box label": Selector(By.CSS_SELECTOR, "label[for=id_q]"),
        "search box": Selector(By.ID, "id_q"),
        # "search button": Selector(By.CSS_SELECTOR, ""),  see BUG TT-1513
    },
    "filters": {
        "itself": Selector(By.ID, "filter-column"),
        "title": Selector(By.CSS_SELECTOR, "#filter-column span"),
        "filter by expertise": Selector(
            By.CSS_SELECTOR, "#filter-column > fieldset:nth-child(2)"
        ),
        "regional expertise": Selector(By.ID, "toggle_id_expertise_regions"),
        "industry expertise": Selector(By.ID, "toggle_id_expertise_industries"),
        "language expertise": Selector(By.ID, "toggle_id_expertise_languages"),
        "international expertise": Selector(By.ID, "toggle_id_expertise_countries"),
        "filter by services": Selector(
            By.CSS_SELECTOR, "#filter-column > fieldset:nth-child(3)"
        ),
        "financial": Selector(By.ID, "toggle_id_expertise_products_services_financial"),
        "management consulting": Selector(
            By.ID, "toggle_id_expertise_products_services_management"
        ),
        "human resources and recruitment": Selector(
            By.ID, "toggle_id_expertise_products_services_human_resources"
        ),
        "publicity and communications": Selector(
            By.ID, "toggle_id_expertise_products_services_publicity"
        ),
        "legal": Selector(By.ID, "toggle_id_expertise_products_services_legal"),
        "business support": Selector(
            By.ID, "toggle_id_expertise_products_services_business_support"
        ),
    },
    "search results": {
        "itself": Selector(By.ID, "companies-column"),
        "result links": Selector(By.CSS_SELECTOR, "#companies-column ul li a"),
    },
}
SELECTORS.update(common_selectors.HEADER_INTERNATIONAL_WO_LANGUAGE_SELECTOR)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.FOOTER_INTERNATIONAL)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)
