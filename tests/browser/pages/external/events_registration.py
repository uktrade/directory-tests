# -*- coding: utf-8 -*-
"""Event Registration Page Object."""
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from directory_tests_shared.utils import check_url_path_matches_template

NAME = "Registration"
SERVICE = Service.EVENTS
TYPE = PageType.FORM
URL = URLs.EVENTS_REGISTRATION.absolute_template
SELECTORS = {}


def should_be_here(driver: WebDriver):
    check_url_path_matches_template(URL, driver.current_url)
