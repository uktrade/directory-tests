# -*- coding: utf-8 -*-
"""International - Industries page"""
from urllib.parse import urljoin

from selenium.webdriver.remote.webdriver import WebDriver

from pages import common_selectors
from pages.common_actions import (
    check_url,
    go_to_url,
    take_screenshot,
)
from settings import EXRED_UI_URL

NAME = "Industries"
SERVICE = "International"
TYPE = "landing"
URL = urljoin(EXRED_UI_URL, "international/industries/")
PAGE_TITLE = "Welcome to great.gov.uk - buy from or invest in the UK"


SELECTORS = {
}
SELECTORS.update(common_selectors.HEADER_INTERNATIONAL)
SELECTORS.update(common_selectors.BETA_BAR)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.FOOTER_INTERNATIONAL)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
