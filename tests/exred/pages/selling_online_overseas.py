# -*- coding: utf-8 -*-
"""Selling Online Overseas Home Page Object."""
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import (
    check_for_expected_sections_elements,
    check_title,
    check_url,
    go_to_url
)
from settings import SELLING_ONLINE_OVERSEAS_UI_URL
from utils import take_screenshot

NAME = "Selling Online Overseas Home page"
URL = urljoin(SELLING_ONLINE_OVERSEAS_UI_URL, "")
PAGE_TITLE = "Welcome to Selling online overseas"

SECTIONS = {
    "expected elements": {
        "title":
            "#content div.outer-container.soft-half--top.text-shadow > h1",
        "what do you sell input": "#search-product",
        "where do you want to sell input": "#search-country",
    }
}


def visit(driver: webdriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    check_title(driver, PAGE_TITLE, exact_match=True)
    check_for_expected_sections_elements(driver, SECTIONS)
