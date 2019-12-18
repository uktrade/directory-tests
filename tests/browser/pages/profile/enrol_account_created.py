# -*- coding: utf-8 -*-
"""Profile - Enrol - Account Created"""
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType
from pages.common_actions import Selector, check_for_sections, check_url, go_to_url

NAME = "Account created"
NAMES = [
    "Account created (LTD, PLC or Royal Charter)",
    "Account created (Sole trader or other type of business)",
    "Account created (UK taxpayer)",
]
SERVICE = Service.PROFILE
TYPE = PageType.FORM
URL = URLs.PROFILE_ENROL_FINISHED.absolute
SubURLs = {
    "account created (ltd, plc or royal charter)": URL,
    "account created (sole trader or other type of business)": URLs.PROFILE_ENROL_NON_CH_COMPANY_FINISHED.absolute,
    "account created (uk taxpayer)": URLs.PROFILE_ENROL_INDIVIDUAL_FINISHED.absolute,
}
PAGE_TITLE = ""

SELECTORS = {
    "confirmation email message": {
        "itself": Selector(By.ID, "success-message-container")
    },
    "publish your business profile": {
        "itself": Selector(By.ID, "next-container"),
        "publish your business profile": Selector(
            By.CSS_SELECTOR,
            "#next-container li:nth-child(1) > a",
            type=ElementType.LINK,
        ),
    },
    "next steps": {
        "itself": Selector(By.ID, "next-container"),
        "next step links": Selector(
            By.CSS_SELECTOR, "#next-container li a", type=ElementType.LINK
        ),
    },
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver, *, page_name: str = None):
    url = SubURLs[page_name.lower()] if page_name else URL
    check_url(driver, url, exact_match=False)
    msg = f"Got 404 on {driver.current_url}"
    assert "This page cannot be found" not in driver.page_source, msg


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)
