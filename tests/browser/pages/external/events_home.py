# -*- coding: utf-8 -*-
"""Events Home Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.common.by import By

from pages.common_actions import (
    Selector,
    check_title,
    check_url,
    go_to_url,
    take_screenshot,
    wait_for_visibility,
)
from settings import EVENTS_UI_URL

NAME = "Home"
SERVICE = "Events"
TYPE = "home"
URL = urljoin(EVENTS_UI_URL, "")
PAGE_TITLE = (
    "Department for International Trade (DIT): exporting from or investing in " "the UK"
)

GREAT_LOGO = Selector(By.CSS_SELECTOR, "#portal-top > h1 > a > img")
SELECTORS = {"general": {"great.gov.uk logo": GREAT_LOGO}}


def visit(driver: webdriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: webdriver):
    wait_for_visibility(driver, by_css=GREAT_LOGO.value, time_to_wait=15)
    check_url(driver, URL, exact_match=True)
    check_title(driver, PAGE_TITLE, exact_match=True)
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)
