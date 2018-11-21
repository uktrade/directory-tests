# -*- coding: utf-8 -*-
"""Existing Office Finder - Home Page Object."""
import logging

from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import check_url, take_screenshot

NAME = "Home"
SERVICE = "EXISTING Office Finder"
TYPE = "home"
URL = "https://www.contactus.trade.gov.uk/office-finder"
SELECTORS = {}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    logging.debug(f"Actor got to the expected page: {URL}")
