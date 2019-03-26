# -*- coding: utf-8 -*-
"""Invest in Great - Contact us - Thank you for your enquiry Page Object."""
import logging
from typing import Dict, List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    check_for_sections,
    check_if_element_is_not_visible,
    check_url,
    take_screenshot,
)
from settings import INVEST_UI_URL

NAME = "Thank you for your enquiry"
NAMES = [
    "High productivity food production",
    "Lightweight structures",
    "Rail infrastructure",
]
SERVICE = "Invest"
TYPE = "HPO Contact us"
URL = urljoin(INVEST_UI_URL, "high-potential-opportunities/")
URLs = {
    "high productivity food production": urljoin(
        URL, "food-production/contact/success/"
    ),
    "lightweight structures": urljoin(URL, "lightweight-structures/contact/success/"),
    "rail infrastructure": urljoin(URL, "rail-infrastructure/contact/success/"),
}
PAGE_TITLE = "High Potential Opportunities - great.gov.uk"

PDF_LINKS = Selector(By.CSS_SELECTOR, "#documents-section a.link")
SELECTORS = {
    "beta bar": {
        "self": Selector(By.ID, "header-beta-bar"),
        "beta bar": Selector(By.CSS_SELECTOR, "#header-beta-bar strong"),
        "feedback": Selector(By.CSS_SELECTOR, "#header-beta-bar a"),
    },
    "confirmation": {
        "itself": Selector(By.ID, "confirmation-section"),
        "heading": Selector(
            By.CSS_SELECTOR, "#confirmation-section div.heading-container"
        ),
    },
    "documents": {
        "itself": Selector(By.ID, "documents-section"),
        "heading": Selector(By.CSS_SELECTOR, "#documents-section h2"),
        "pdf links": PDF_LINKS,
        "description": Selector(By.CSS_SELECTOR, "#documents-section h3 ~ span"),
    },
    "report this page": {
        "self": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "report link": Selector(By.CSS_SELECTOR, "section.error-reporting a"),
    },
}

UNEXPECTED_ELEMENTS = {
    "breadcrumbs": {"itself": Selector(By.CSS_SELECTOR, "div.breadcrumbs")}
}


def should_be_here(driver: WebDriver, *, page_name: str):
    take_screenshot(driver, PAGE_TITLE)
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def should_not_see_section(driver: WebDriver, name: str):
    section = UNEXPECTED_ELEMENTS[name.lower()]
    for key, selector in section.items():
        check_if_element_is_not_visible(driver, selector, element_name=key)


def download_all_pdfs(driver: WebDriver) -> List[Dict[str, bytes]]:
    import requests

    anchors = driver.find_elements(by=PDF_LINKS.by, value=PDF_LINKS.value)
    hrefs = [anchor.get_property("href") for anchor in anchors]
    responses = [requests.get(href) for href in hrefs]
    assert all(response.status_code == 200 for response in responses)
    logging.debug(f"Successfully downloaded all {len(hrefs)} PDFs")
    pdfs = [{"href": response.url, "pdf": response.content} for response in responses]
    return pdfs
