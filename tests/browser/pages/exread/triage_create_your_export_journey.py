# -*- coding: utf-8 -*-
"""Triage - Create your export journey Page Object."""
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import (
    check_for_expected_sections_elements,
    check_for_section,
    check_if_element_is_not_visible,
    check_title,
    check_url,
    find_and_click_on_page_element,
    go_to_url,
    take_screenshot,
)
from settings import EXRED_UI_URL

NAME = "Create your export journey"
URL = urljoin(EXRED_UI_URL, "triage/")
PAGE_TITLE = "Your export journey - great.gov.uk"

START_NOW = "#start-now-container > a"
REGISTER = "#start-now-container > div > a:nth-child(2)"
SIGN_IN = "#start-now-container > div > a:nth-child(3)"
REPORT_THIS_PAGE = "#error-reporting-section-contact-us"

SECTIONS = {
    "description": {
        "title": "#start-now-container > h1",
        "description": "#start-now-container > p",
        # "list of benefits": "#start-now-container > ul",
    },
    "start now": {"start now button": START_NOW},
    "save progress": {"register link": REGISTER, "sign-in link": SIGN_IN},
    "report this page": {"report this page link": REPORT_THIS_PAGE},
}


def visit(driver: webdriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_see_section(driver: webdriver, name: str):
    check_for_section(driver, all_sections=SECTIONS, sought_section=name)


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    check_title(driver, PAGE_TITLE, exact_match=False)
    check_for_expected_sections_elements(driver, SECTIONS)


def click_on_page_element(driver: webdriver, element_name: str):
    find_and_click_on_page_element(driver, SECTIONS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)


def should_not_see_section(driver: webdriver, name: str):
    section = SECTIONS[name.lower()]
    for key, selector in section.items():
        check_if_element_is_not_visible(driver, by_css=selector, element_name=key)
