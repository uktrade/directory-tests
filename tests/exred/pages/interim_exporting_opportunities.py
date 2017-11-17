# -*- coding: utf-8 -*-
"""Interim Export Opportunities Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from settings import EXRED_UI_URL
from utils import assertion_msg, take_screenshot

NAME = "ExRed Interim Export Opportunities"
URL = urljoin(EXRED_UI_URL, "export-opportunities")

EXPORT_OPPORTUNITIES_BUTTON = "a.button-primary"
REPORT_THIS_PAGE_LINK = "section.error-reporting a"
EXPECTED_ELEMENTS = {
    "title": "#content article > h1",
    "description": "#content article > p",
    "links to selected articles": "#content article > ul",
    "go to export opportunities": EXPORT_OPPORTUNITIES_BUTTON,
    "is there anything wrong with this page?": REPORT_THIS_PAGE_LINK
}


def should_be_here(driver: webdriver):
    for element_name, element_selector in EXPECTED_ELEMENTS.items():
        element = driver.find_element_by_css_selector(element_selector)
        with assertion_msg(
                "It looks like '%s' element is not visible on %s",
                element_name, NAME):
            assert element.is_displayed()
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def go_to_export_opportunities(driver: webdriver):
    link = driver.find_element_by_css_selector(EXPORT_OPPORTUNITIES_BUTTON)
    link.click()
    take_screenshot(driver, NAME + " after going to Export Opportunities")
