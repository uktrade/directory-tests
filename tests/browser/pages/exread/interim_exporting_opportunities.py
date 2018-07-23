# -*- coding: utf-8 -*-
"""Interim Export Opportunities Page Object."""
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import (
    check_for_expected_elements,
    check_title,
    check_url,
    find_element,
    go_to_url,
    take_screenshot,
    wait_for_page_load_after_action,
    wait_for_visibility,
)
from settings import EXRED_UI_URL

NAME = "Interim Export Opportunities"
SERVICE = "Export Readiness"
TYPE = "interim"
URL = urljoin(EXRED_UI_URL, "export-opportunities/")
PAGE_TITLE = "Make sure you're export ready - great.gov.uk"

SERVICE_BUTTON = "a.button-primary"
REPORT_THIS_PAGE_LINK = "section.error-reporting a"
EXPECTED_ELEMENTS = {
    "title": "#content h1",
    "description": "#content p",
    "links to selected articles": "#content ul.list",
    "go to export opportunities": SERVICE_BUTTON,
    "is there anything wrong with this page?": REPORT_THIS_PAGE_LINK,
}
SELECTORS = {}


def visit(driver: webdriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    check_title(driver, PAGE_TITLE, exact_match=False)
    check_for_expected_elements(driver, EXPECTED_ELEMENTS)


def go_to_service(driver: webdriver):
    service_button = find_element(driver, by_css=SERVICE_BUTTON)
    wait_for_visibility(driver, by_css=SERVICE_BUTTON, time_to_wait=10)
    with wait_for_page_load_after_action(driver):
        service_button.click()
    take_screenshot(driver, NAME + " after going to Export Opportunities")
