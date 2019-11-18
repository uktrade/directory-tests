# -*- coding: utf-8 -*-
"""GOV.UK - Prepare your business or organisation for Brexit."""
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared.enums import PageType, Service
from pages.common_actions import check_url, go_to_url

NAME = "Prepare your business or organisation for Brexit"
SERVICE = Service.GOVUK
TYPE = PageType.HOME
URL = "https://www.gov.uk/business-uk-leaving-eu"
SELECTORS = {}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL)
