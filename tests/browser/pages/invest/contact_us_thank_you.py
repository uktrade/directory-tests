# -*- coding: utf-8 -*-
"""Invest in Great - Thank you for your message Page Object."""
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import common_selectors
from pages.common_actions import Selector, check_url, go_to_url

NAME = "Thank you for your message"
SERVICE = Service.INVEST
TYPE = PageType.THANK_YOU
URL = URLs.INVEST_CONTACT_SUCCESS.absolute
PAGE_TITLE = ""
SELECTORS = {
    "success message": {"itself": Selector(By.CSS_SELECTOR, "section.contact-success")}
}
SELECTORS.update(common_selectors.INVEST_HEADER)
SELECTORS.update(common_selectors.INTERNATIONAL_HERO)
SELECTORS.update(common_selectors.ERROR_REPORTING)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)
