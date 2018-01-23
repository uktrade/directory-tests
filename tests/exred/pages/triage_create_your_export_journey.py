# -*- coding: utf-8 -*-
"""Triage - Create your export journey Page Object."""
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import (
    check_for_expected_sections_elements,
    check_for_section,
    check_title,
    check_url,
    go_to_url
)
from settings import EXRED_UI_URL
from utils import find_element, take_screenshot

NAME = "Create your export journey"
URL = urljoin(EXRED_UI_URL, "custom/")
PAGE_TITLE = "Your export journey - great.gov.uk"

START_NOW = "#start-now-container > a"
REGISTER = "#start-now-container > div > a:nth-child(2)"
SIGN_IN = "#start-now-container > div > a:nth-child(3)"
REPORT_THIS_PAGE = "#error-reporting-section-contact-us"

SECTIONS = {
    "description": {
        "title": "#start-now-container > h1",
        "description": "#start-now-container > p:nth-child(3)",
        "list of benefits": "#start-now-container > ul",
    },
    "start now": {
        "start now button": START_NOW,
        "register link": REGISTER,
        "sign-in link": SIGN_IN
    },
    "report this page": {
        "report this page link": REPORT_THIS_PAGE
    }
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


def start_now(driver: webdriver):
    star_now = find_element(driver, by_css=START_NOW)
    star_now.click()
    take_screenshot(driver, NAME)
