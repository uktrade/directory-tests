# -*- coding: utf-8 -*-
"""Interim Export Opportunities Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from settings import EXRED_UI_URL
from utils import (
    assertion_msg,
    find_element,
    take_screenshot,
    wait_for_visibility
)

NAME = "ExRed Interim Export Opportunities"
URL = urljoin(EXRED_UI_URL, "export-opportunities")

SERVICE_BUTTON = "a.button-primary"
REPORT_THIS_PAGE_LINK = "section.error-reporting a"
EXPECTED_ELEMENTS = {
    "title": "#content article > h1",
    "description": "#content article > p",
    "links to selected articles": "#content article > ul",
    "go to export opportunities": SERVICE_BUTTON,
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


def go_to_service(driver: webdriver):
    service_button = find_element(driver, by_css=SERVICE_BUTTON)
    wait_for_visibility(driver, by_css=SERVICE_BUTTON, time_to_wait=10)
    service_button.click()
    take_screenshot(driver, NAME + " after going to Export Opportunities")
