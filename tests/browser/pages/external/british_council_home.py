# -*- coding: utf-8 -*-
"""British Council Home Page Object."""
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared.enums import PageType, Service
from pages.common_actions import check_url, go_to_url

NAME = "Home"
SERVICE = Service.BRITISH_COUNCIL
TYPE = PageType.HOME
URL = "https://study-uk.britishcouncil.org/"
SELECTORS = {}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=False)
