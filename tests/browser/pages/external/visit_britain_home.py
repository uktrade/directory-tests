# -*- coding: utf-8 -*-
"""Visit Britain Home Page Object."""
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared.enums import PageType, Service
from pages.common_actions import check_url

NAME = "Home"
SERVICE = Service.VISIT_BRITAIN
TYPE = PageType.HOME
URL = "https://www.visitbritain.com/"
SELECTORS = {}


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=False)
