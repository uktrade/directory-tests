# -*- coding: utf-8 -*-
"""Events Event Page Object."""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from directory_tests_shared.utils import check_url_path_matches_template
from pages.common_actions import Selector

NAME = "Event"
SERVICE = Service.EVENTS
TYPE = PageType.EVENT
URL = URLs.EVENTS_EVENT.absolute_template
GREAT_LOGO = Selector(By.CSS_SELECTOR, "div.event-logo")
SELECTORS = {
    "general": {"great.gov.uk logo": GREAT_LOGO},
    "breadcrumbs": Selector(By.CSS_SELECTOR, ".breadcrumbs div>a"),
}


def should_be_here(driver: WebDriver):
    check_url_path_matches_template(URL, driver.current_url)
