# -*- coding: utf-8 -*-
"""Find a Supplier - Generic Company Profile Page Object."""
import logging
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    check_url,
    find_and_click_on_page_element,
    take_screenshot,
)
from settings import DIRECTORY_UI_SUPPLIER_URL

NAME = "Company Profile"
SERVICE = "Find a Supplier"
TYPE = "profile"
URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "suppliers/")

SELECTORS = {
    "name": {"itself": Selector(By.ID, "company-name")},
    "company details": {
        "itself": Selector(By.ID, "main-content"),
        "logo": Selector(By.ID, "cover-image-container"),
        "contact company": Selector(
            By.CSS_SELECTOR, "#contact-company-container a"
        ),
        "about company": Selector(By.ID, "about-company-container"),
    },
    "online-profiles": {
        "itself": Selector(By.ID, "online-profiles"),
    },
    "description": {
        "itself": Selector(By.ID, "company-description-container"),
        "read more": Selector(
            By.CSS_SELECTOR, "#company-description-container a"
        ),
    },
    "report profile": {
        "itself": Selector(By.CSS_SELECTOR, "div.ed-report-profile-container"),
        "report profile": Selector(
            By.CSS_SELECTOR, "div.ed-report-profile-container a[href^=mailto]"
        ),
    },
}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)
