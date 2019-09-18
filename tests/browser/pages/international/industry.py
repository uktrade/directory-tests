# -*- coding: utf-8 -*-
"""International - Industry"""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import Services, common_selectors
from pages.common_actions import (
    Selector,
    assertion_msg,
    check_for_sections,
    check_url,
    find_and_click_on_page_element,
    find_elements,
    find_selector_by_name,
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
    "Energy",
    "Engineering and manufacturing",
    "Financial and professional services",
    "Financial services",
    "Food and drink",
    "Health and Life Sciences",
    "Healthcare and Life Sciences",
    "Industry",
    "Legal services",
    "Maritime",
    "Nuclear energy",
    "Real Estate",
    "Retail",
    "Space",
    "Sports economy",
    "Technology",
]
SERVICE = Services.INTERNATIONAL
TYPE = "industry"
URL = urljoin(EXRED_UI_URL, "international/content/about-uk/industries/")
PAGE_TITLE = "great.gov.uk International - "


URLs = {
    "industry": URL,
    "aerospace": urljoin(URL, "aerospace/"),
    "agricultural technology": urljoin(URL, "agricultural-technology/"),
    "automotive": urljoin(URL, "automotive/"),
    "creative industries": urljoin(URL, "creative-industries/"),
    "creative services": urljoin(URL, "creative-services/"),
    "cyber security": urljoin(URL, "cyber-security/"),
    "education": urljoin(URL, "education/"),
    "energy": urljoin(URL, "energy/"),
    "engineering and manufacturing": urljoin(URL, "engineering-and-manufacturing/"),
    "financial and professional services": urljoin(URL, "financial-services/"),
    "financial services": urljoin(URL, "financial-services/"),
    "food and drink": urljoin(URL, "food-and-drink/"),
    "health and life sciences": urljoin(URL, "health-and-life-sciences/"),
    "healthcare and life sciences": urljoin(URL, "health-and-life-sciences/"),
    "legal services": urljoin(URL, "legal-services/"),
    "maritime": urljoin(URL, "maritime/"),
    "nuclear energy": urljoin(URL, "nuclear-energy/"),
    "real estate": urljoin(URL, "real-estate/"),
    "retail": urljoin(URL, "retail/"),
    "space": urljoin(URL, "space/"),
    "sports economy": urljoin(URL, "sports-economy/"),
    "technology": urljoin(URL, "technology/"),
}

SELECTORS = {
    "industry breadcrumbs": {
        "great.gov.uk international": Selector(
            By.CSS_SELECTOR, "#breadcrumb-section ol > li:nth-child(1) > a"
        ),
        "industries": Selector(
            By.CSS_SELECTOR, "#breadcrumb-section ol > li:nth-child(2) > a"
        ),
    },
    "content": {
        "section 1": Selector(By.ID, "sector-section-one"),
        "section 2": Selector(By.ID, "sector-section-two"),
        "section statistics": Selector(By.ID, "sector-statistics-section"),
    },
    "next steps": {
        "next steps": Selector(By.ID, "sector-next-steps-section"),
        "invest in the uk": Selector(
            By.CSS_SELECTOR, "#sector-next-steps-section div:nth-child(1) > a"
        ),
        "buy from the uk": Selector(
            By.CSS_SELECTOR, "#sector-next-steps-section div:nth-child(2) > a"
        ),
    },
}
SELECTORS.update(common_selectors.INTERNATIONAL_HEADER)
SELECTORS.update(common_selectors.INTERNATIONAL_HERO)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.INTERNATIONAL_FOOTER)


def visit(driver: WebDriver, *, page_name: str = None):
    url = URLs[page_name] if page_name else URL
    visit_url(driver, url)


def should_be_here(driver: WebDriver, *, page_name: str):
    take_screenshot(driver, PAGE_TITLE)
    url = URLs[page_name.lower()] if page_name else URL
    check_url(driver, url, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def clean_name(name: str) -> str:
    return name.split(" - ")[1].strip()


def should_see_content_for(driver: WebDriver, industry_name: str):
    source = driver.page_source
    industry_name = clean_name(industry_name)
    logging.debug("Looking for: {}".format(industry_name))
    with assertion_msg(
        "Expected to find term '%s' in the source of the page %s",
        industry_name,
        driver.current_url,
    ):
        assert industry_name.lower() in source.lower()


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)
