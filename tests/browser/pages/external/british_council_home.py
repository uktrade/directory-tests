# -*- coding: utf-8 -*-
"""British Council Home Page Object."""
import logging

from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import check_url, go_to_url, take_screenshot

NAME = "Home"
SERVICE = "British Council"
TYPE = "home"
URL = "https://study-uk.britishcouncil.org/"
SELECTORS = {}


def visit(driver: WebDriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=False)
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)
