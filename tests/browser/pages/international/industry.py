# -*- coding: utf-8 -*-
"""International - Industry"""
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

NAME = "Industry"
NAMES = [
    "Aerospace",
    "Agricultural technology",
    "Automotive",
    "Creative industries",
    "Cyber security",
    "Education",
    "Engineering and manufacturing",
    "Financial services",
    "Food and drink",
    "Health and Life Sciences",
    "Legal services",
    "Maritime",
    "Nuclear energy",
    "Retail",
    "Space",
    "Sports economy",
    "Technology",
]
SERVICE = "International"
TYPE = "industry"
URL = urljoin(EXRED_UI_URL, "international/content/industries/")
PAGE_TITLE = "great.gov.uk International - "


URLs = {
    "aerospace": urljoin(URL, "aerospace/"),
    "agricultural technology": urljoin(URL, "agricultural-technology/"),
    "automotive": urljoin(URL, "automotive/"),
    "creative industries": urljoin(URL, "creative-industries/"),
    "cyber security": urljoin(URL, "cyber-security/"),
    "education": urljoin(URL, "education"),
    "engineering and manufacturing": urljoin(URL, "engineering-and-manufacturing/"),
    "financial services": urljoin(URL, "financial-services"),
    "food and drink": urljoin(URL, "food-and-drink/"),
    "health and life sciences": urljoin(URL, "health-and-life-sciences/"),
    "legal services": urljoin(URL, "legal-services/"),
    "maritime": urljoin(URL, "maritime/"),
    "nuclear energy": urljoin(URL, "nuclear-energy/"),
    "retail": urljoin(URL, "retail/"),
    "space": urljoin(URL, "space/"),
    "sports economy": urljoin(URL, "sports-economy/"),
    "technology": urljoin(URL, "technology/"),
}


SELECTORS = {
}
SELECTORS.update(common_selectors.HEADER_INTERNATIONAL)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.FOOTER_INTERNATIONAL)


def visit(driver: WebDriver, *, page_name: str = None):
    url = URLs[page_name.split(" - ")[1].lower()] if page_name else URL
    visit_url(driver, url)


def should_be_here(driver: WebDriver, *, page_name: str):
    take_screenshot(driver, PAGE_TITLE)
    url = URLs[page_name.lower()] if page_name else URL
    check_url(driver, url, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)
