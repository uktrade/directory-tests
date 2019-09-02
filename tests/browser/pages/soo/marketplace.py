# -*- coding: utf-8 -*-
"""Selling Online Overseas Home Page Object."""
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import Services
from pages.common_actions import (
    Selector,
    check_url,
    find_and_click_on_page_element,
    take_screenshot,
)
from settings import SELLING_ONLINE_OVERSEAS_UI_URL

SERVICE = Services.SOO
TYPE = "search"
NAME = "Marketplace"
URL = urljoin(SELLING_ONLINE_OVERSEAS_UI_URL, "markets/details")
PAGE_TITLE = "Marketplace details | Selling Online Overseas"


SELECTORS = {
    "expected elements": {
        "marketplace": Selector(By.CSS_SELECTOR, "div.market-item h1"),
        "apply now": Selector(By.CSS_SELECTOR, "#content div.market-item a.button "),
    }
}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)


def click_on_page_element(driver, element_name):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)
