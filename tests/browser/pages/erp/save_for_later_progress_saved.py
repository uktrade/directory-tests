# -*- coding: utf-8 -*-
"""ERP - Save for later - Progress saved"""
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType, common_selectors
from pages.common_actions import Selector, check_for_sections, check_url

NAME = "Progress saved"
SERVICE = Service.ERP
TYPE = PageType.THANK_YOU
URL = URLs.ERP_SAVE_FOR_LATER.absolute
PAGE_TITLE = ""

SELECTORS = {
    "confirmation": {
        "heading": Selector(By.CSS_SELECTOR, "#content h1"),
        "what happens next": Selector(By.CSS_SELECTOR, "#content h2"),
        "continue": Selector(
            By.CSS_SELECTOR, "#content h2 ~ a", type=ElementType.SUBMIT
        ),
    }
}
SELECTORS.update(common_selectors.ERP_HEADER)
SELECTORS.update(common_selectors.ERP_BETA)
SELECTORS.update(common_selectors.ERP_FOOTER)


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=False)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)
