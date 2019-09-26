# -*- coding: utf-8 -*-
"""Profile - Edit Company Profile"""
import logging

from directory_tests_shared import URLs
from directory_tests_shared.enums import Service
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import check_url, go_to_url, take_screenshot

NAME = "Edit Company Profile"
SERVICE = Service.PROFILE
TYPE = "profile"
URL = URLs.PROFILE_BUSINESS_PROFILE.absolute
PAGE_TITLE = "Business profile - great.gov.uk"

SELECTORS = {}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", NAME)
