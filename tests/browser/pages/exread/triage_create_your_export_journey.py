# -*- coding: utf-8 -*-
"""Triage - Create your export journey Page Object."""
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    check_for_expected_sections_elements,
    check_for_section,
    check_if_element_is_not_visible,
    check_title,
    check_url,
    find_and_click_on_page_element,
    go_to_url,
    take_screenshot,
    Selector
)
from settings import EXRED_UI_URL

NAME = "Create your export journey"
SERVICE = "Export Readiness"
TYPE = "triage"
URL = urljoin(EXRED_UI_URL, "triage/")
PAGE_TITLE = "Your export journey - great.gov.uk"

START_NOW = Selector(By.CSS_SELECTOR, "#start-now-container > a")
REGISTER = Selector(By.CSS_SELECTOR, "#start-now-container > div > a:nth-child(2)")
SIGN_IN = Selector(By.CSS_SELECTOR, "#start-now-container > div > a:nth-child(3)")
REPORT_THIS_PAGE = Selector(By.CSS_SELECTOR, "#error-reporting-section-contact-us")

SELECTORS = {
    "description": {
        "title": Selector(By.CSS_SELECTOR, "#start-now-container > h1"),
        "description": Selector(By.CSS_SELECTOR, "#start-now-container > p"),
        "list of benefits": Selector(By.CSS_SELECTOR, "#start-now-container > ul"),
    },
    "start now": {"start now button": START_NOW},
    "save progress": {"register link": REGISTER, "sign-in link": SIGN_IN},
    "report this page": {"report this page link": REPORT_THIS_PAGE},
}


def visit(driver: WebDriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_see_section(driver: WebDriver, name: str):
    check_for_section(driver, all_sections=SELECTORS, sought_section=name)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    check_title(driver, PAGE_TITLE, exact_match=False)
    check_for_expected_sections_elements(driver, SELECTORS)


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)


def should_not_see_section(driver: WebDriver, name: str):
    section = SELECTORS[name.lower()]
    for key, selector in section.items():
        check_if_element_is_not_visible(driver, selector, element_name=key)
