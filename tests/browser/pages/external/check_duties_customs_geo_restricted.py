# -*- coding: utf-8 -*-
"""Check duties and customs - Access Geo Restricted Page Object."""
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared.enums import PageType, Service
from pages.common_actions import check_url, go_to_url

NAME = "Access Geo Restricted"
SERVICE = Service.CHECK_DUTIES_CUSTOMS
TYPE = PageType.ERROR
URL = "https://www.check-duties-customs-exporting-goods.service.gov.uk/georestricted"
SELECTORS = {}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL)
