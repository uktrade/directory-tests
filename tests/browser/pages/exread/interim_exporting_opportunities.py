# -*- coding: utf-8 -*-
"""Interim Export Opportunities Page Object."""
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
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

SERVICE_BUTTON = Selector(By.CSS_SELECTOR, "a.button-primary")
REPORT_THIS_PAGE_LINK = Selector(By.CSS_SELECTOR, "section.error-reporting a")
SELECTORS = {
    "general": {
        "title": Selector(By.CSS_SELECTOR, "#content h1"),
        "description": Selector(By.CSS_SELECTOR, "#content p"),
        "links to selected articles": Selector(By.CSS_SELECTOR, "#content ul.list"),
        "go to export opportunities": SERVICE_BUTTON,
        "is there anything wrong with this page?": REPORT_THIS_PAGE_LINK,
    }
}


def visit(driver: WebDriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)


def go_to_service(driver: WebDriver):
    service_button = find_element(driver, SERVICE_BUTTON)
    wait_for_visibility(driver, SERVICE_BUTTON, time_to_wait=10)
    with wait_for_page_load_after_action(driver):
        service_button.click()
    take_screenshot(driver, NAME + " after going to Export Opportunities")
