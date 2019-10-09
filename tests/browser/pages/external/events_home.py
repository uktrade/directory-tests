# -*- coding: utf-8 -*-
"""Events Home Page Object."""
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import Service
from pages.common_actions import (
    Selector,
    check_url,
    go_to_url,
    take_screenshot,
    wait_for_visibility,
)

NAME = "Home"
SERVICE = Service.EVENTS
TYPE = "home"
URL = URLs.EVENTS_LANDING.absolute
GREAT_LOGO = Selector(By.CSS_SELECTOR, "div.event-logo")
SELECTORS = {"general": {"great.gov.uk logo": GREAT_LOGO}}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    wait_for_visibility(driver, GREAT_LOGO, time_to_wait=15)
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)
