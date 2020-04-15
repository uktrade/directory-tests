# -*- coding: utf-8 -*-
"""Invest in Great - Contact us - Thank you for your enquiry Page Object."""
import logging
from typing import Dict, List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import common_selectors
from pages.common_actions import Selector, check_for_sections, check_url

NAME = "Thank you for your enquiry"
NAMES = [
    "High productivity food production",
    "Lightweight structures",
    "Rail infrastructure",
]
SERVICE = Service.INVEST
TYPE = PageType.CONTACT_US
URL = URLs.INVEST_HPO_CONTACT_THANK_YOU.absolute
SubURLs = {
    "advanced food production": URL,
    "lightweight structures": URL,
    "rail infrastructure": URL,
}
PAGE_TITLE = "High Potential Opportunities - great.gov.uk"

PDF_LINKS = Selector(By.CSS_SELECTOR, "#documents-section a.link")
SELECTORS = {
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
}
SELECTORS.update(common_selectors.INVEST_HEADER)
SELECTORS.update(common_selectors.BETA_BAR)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.INVEST_FOOTER)


def should_be_here(driver: WebDriver, *, page_name: str):
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def download_all_pdfs(driver: WebDriver) -> List[Dict[str, bytes]]:
    import requests

    anchors = driver.find_elements(by=PDF_LINKS.by, value=PDF_LINKS.value)
    hrefs = [anchor.get_property("href") for anchor in anchors]
    responses = [requests.get(href) for href in hrefs]
    assert all(response.status_code == 200 for response in responses)
    logging.debug(f"Successfully downloaded all {len(hrefs)} PDFs")
    pdfs = [{"href": response.url, "pdf": response.content} for response in responses]
    return pdfs
