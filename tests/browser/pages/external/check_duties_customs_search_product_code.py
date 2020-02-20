# -*- coding: utf-8 -*-
"""Check duties and customs Home Page Object."""
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared.enums import PageType, Service
from directory_tests_shared.utils import check_url_path_matches_template
from pages.common_actions import go_to_url

NAME = "Search product code"
SERVICE = Service.CHECK_DUTIES_CUSTOMS
TYPE = PageType.SEARCH
URL = "https://www.check-duties-customs-exporting-goods.service.gov.uk/searchproduct?d={country}"
SELECTORS = {}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url_path_matches_template(URL, driver.current_url)
