# -*- coding: utf-8 -*-
"""Selling Online Overseas Home Page Object."""
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    check_url,
    go_to_url,
    take_screenshot,
)
from settings import SELLING_ONLINE_OVERSEAS_UI_URL

NAME = "Home"
URL = urljoin(SELLING_ONLINE_OVERSEAS_UI_URL, "")
SERVICE = "Selling Online Overseas"
TYPE = "home"
PAGE_TITLE = "Welcome to Selling online overseas"

SELECTORS = {
    "expected elements": {
        "hero section": Selector(By.CSS_SELECTOR, ".hero-content"),
        "what do you sell input": Selector(By.ID, "search-product"),
        "where do you want to sell input": Selector(By.ID, "search-country"),
    }
}


def visit(driver: WebDriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
