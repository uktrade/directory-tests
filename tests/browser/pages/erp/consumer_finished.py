# -*- coding: utf-8 -*-
"""ERP - Finished - UK consumer"""
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import common_selectors
from pages.common_actions import (
    Selector,
    check_for_sections,
    check_url,
    find_and_click_on_page_element,
    take_screenshot,
)

NAME = "Finished (UK consumer)"
SERVICE = Service.ERP
TYPE = PageType.FORM
URL = URLs.ERP_CONSUMER_FINISHED.absolute
PAGE_TITLE = ""

SELECTORS = {
    "form submitted": {
        "heading": Selector(By.CSS_SELECTOR, "#content h1"),
        "print a copy now": Selector(By.PARTIAL_LINK_TEXT, "print a copy now"),
        "submit another form": Selector(By.PARTIAL_LINK_TEXT, "Submit another form"),
        "return to gov.uk": Selector(By.PARTIAL_LINK_TEXT, "Return to Gov.uk"),
    }
}
SELECTORS.update(common_selectors.ERP_HEADER)
SELECTORS.update(common_selectors.ERP_BETA)
SELECTORS.update(common_selectors.ERP_FOOTER)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)
