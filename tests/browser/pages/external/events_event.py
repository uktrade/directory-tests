# -*- coding: utf-8 -*-
"""Events Event Page Object."""
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages.common_actions import Selector, check_url

NAME = "Event"
SERVICE = Service.EVENTS
TYPE = PageType.EVENT
URL = URLs.EVENTS_EVENT.absolute
GREAT_LOGO = Selector(By.CSS_SELECTOR, "div.event-logo")
SELECTORS = {
    "general": {"great.gov.uk logo": GREAT_LOGO},
    "breadcrumbs": Selector(By.CSS_SELECTOR, ".breadcrumbs div>a"),
}


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)
