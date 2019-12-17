# -*- coding: utf-8 -*-
"""ERP - Landing"""
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import common_selectors
from pages.common_actions import Selector, check_for_sections, check_url, go_to_url

NAME = "Landing"
SERVICE = Service.ERP
TYPE = PageType.LANDING
URL = URLs.ERP_LANDING.absolute
PAGE_TITLE = ""

SELECTORS = {
    "description": {
        "heading": Selector(By.CSS_SELECTOR, "#content h1"),
        "description": Selector(By.CSS_SELECTOR, "#content h1 ~ p"),
        "start now": Selector(By.CSS_SELECTOR, "#content h1 ~ a"),
    }
}
SELECTORS.update(common_selectors.ERP_HEADER)
SELECTORS.update(common_selectors.ERP_BETA)
SELECTORS.update(common_selectors.ERP_BREADCRUMBS)
SELECTORS.update(common_selectors.ERP_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)
